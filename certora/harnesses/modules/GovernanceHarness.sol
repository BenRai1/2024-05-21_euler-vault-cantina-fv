// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Governance.sol";
import {IIRM} from "../../../src/InterestRateModels/IIRM.sol";



contract GovernanceHarness is Governance, AbstractBaseHarness {
    uint256 private constant SHARES_MASK = 0x000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    
    using TypesLib for uint16;
    constructor(Integrations memory integrations) Governance (integrations) {}

    function getOnBehalfOfAccountHarness() external returns (address onBehalfOfAccount) {
        return EVCAuthenticateGovernor();
    }

    function getCFG_MAX_VALUEHarness() external returns (uint32) {
        return CFG_MAX_VALUE;
    }

    function getOP_MAX_VALUEHarness() external returns (uint32) {
        return OP_MAX_VALUE;
    }

    function getMAX_SANE_AMOUNTHarness() external returns (uint256) {
        return MAX_SANE_AMOUNT;
    }

    function getGUARANTEED_INTEREST_FEE_MINHarness() external returns (uint16) {
        return GUARANTEED_INTEREST_FEE_MIN;
    }

    function getGUARANTEED_INTEREST_FEE_MAXHarness() external returns (uint16) {
        return GUARANTEED_INTEREST_FEE_MAX;
    }


    function toConfigAmountHarness(uint16 value) external returns (ConfigAmount) {
        return value.toConfigAmount();
    }

    function getLTVHarness(LTVConfig memory self, bool liquidation) external returns (ConfigAmount) {
        return self.getLTV(liquidation);
    }

    function getCurrentLTVConfigHarness(address collateral) external returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function wrapAmountCapHarness(uint16 value) external returns (AmountCap) {
        return AmountCap.wrap(value);
    }

    function resolveAmountCapHarness(AmountCap self) external returns (uint256) {
        return self.resolve();
    }

    function wrapFlagsHarness(uint32 value) external pure returns (Flags) {
        return Flags.wrap(value);
    }

    function getHookTargetSelectorHarness() external returns (bytes4) {
        return this.isHookTarget.selector;
    }

    function isHookTarget() external pure returns (bytes4) {
        return this.isHookTarget.selector;
    }

    function isValidInterestFeeHarness(uint16 interestFee) external returns (bool) {
        return protocolConfig.isValidInterestFee(address(this), interestFee);
    }

    function getVaultCacheHarness() external returns (VaultCache memory) {
        return updateVault();
    }

    function getInterestRateHarness() external returns (uint72) {
        return  vaultStorage.interestRate;
    }

    //@audit not sure if this works, check again
    //i: modified from BorrowUtils.computeInterestRate
    function getTargetInterestRateHarness(address irm, VaultCache memory vaultCache) external returns (uint256) {
         // single sload
        uint256 newInterestRate = 0;

        if (irm != address(0)) { //i: if fallse, interestRate should be 0
            (bool success, bytes memory data) = irm.call(
                abi.encodeCall(
                    IIRM.computeInterestRate,
                    (address(this), vaultCache.cash.toUint(), vaultCache.totalBorrows.toAssetsUp().toUint())
                )
            );

            if (success && data.length >= 32) {
                newInterestRate = abi.decode(data, (uint256));
                if (newInterestRate > MAX_ALLOWED_INTEREST_RATE) newInterestRate = MAX_ALLOWED_INTEREST_RATE;
                vaultStorage.interestRate = uint72(newInterestRate);
            }
        }

        return newInterestRate;
    }

    function calculateLiquidationLTVHarness(LTVConfig memory self, bool liquidation) external returns (ConfigAmount) {
        if (!liquidation) {
            return self.borrowLTV;
        }

        if (block.timestamp >= self.targetTimestamp || self.liquidationLTV >= self.initialLiquidationLTV) {
            return self.liquidationLTV;
        }

        uint256 currentLiquidationLTV = self.initialLiquidationLTV.toUint16();

        unchecked {
            uint256 targetLiquidationLTV = self.liquidationLTV.toUint16();
            uint256 timeRemaining = self.targetTimestamp - block.timestamp;

            // targetLiquidationLTV < initialLiquidationLTV and timeRemaining <= rampDuration
            currentLiquidationLTV = targetLiquidationLTV
                + (currentLiquidationLTV - targetLiquidationLTV) * timeRemaining / self.rampDuration;
        }

        // because ramping happens only when liquidation LTV decreases, it's safe to down-cast the new value
        return ConfigAmount.wrap(uint16(currentLiquidationLTV));
    }

    function getUserStorageDataHarness(address user) external returns (PackedUserSlot) {
        return vaultStorage.users[user].data;
    }

    function getGovernorReceiverHarness() external returns (address) {
        return vaultStorage.feeReceiver;
    }

    function getTotalSharesHarness() public returns (Shares){
    return vaultStorage.totalShares;
    }

    function getCurrentVaultCacheHarness() external returns (VaultCache memory){
        VaultCache memory vaultCache;
        (vaultCache.asset, vaultCache.oracle, vaultCache.unitOfAccount) = ProxyUtils.metadata();
        vaultCache.lastInterestAccumulatorUpdate = vaultStorage.lastInterestAccumulatorUpdate;
        vaultCache.cash = vaultStorage.cash;
        vaultCache.totalBorrows = vaultStorage.totalBorrows;
        vaultCache.totalShares = vaultStorage.totalShares;
        vaultCache.supplyCap = vaultStorage.supplyCap.resolve();
        vaultCache.borrowCap = vaultStorage.borrowCap.resolve();
        vaultCache.hookedOps = vaultStorage.hookedOps;
        vaultCache.snapshotInitialized = true;
        vaultCache.accumulatedFees = vaultStorage.accumulatedFees;
        vaultCache.configFlags = vaultStorage.configFlags;
        vaultCache.interestAccumulator = vaultStorage.interestAccumulator;
        return vaultCache;
    }

    function calculateProtocolFeeHarness(address governorReceiver, uint16 protocolFee) external returns (uint16) {
        if (governorReceiver == address(0)) {
            protocolFee = CONFIG_SCALE; 
        } else if (protocolFee > MAX_PROTOCOL_FEE_SHARE) {
            protocolFee = MAX_PROTOCOL_FEE_SHARE;
        }
        return protocolFee;
    }

    function calculateSharesToMoveHarness(Shares accumulatedFees, uint16 protocolFee) external returns (Shares, Shares) {
        Shares governorShares = accumulatedFees.mulDiv(CONFIG_SCALE - protocolFee, CONFIG_SCALE);
        Shares protocolShares = accumulatedFees - governorShares;
        return (governorShares, protocolShares);
    }
    
    function unpackBalanceHarness(PackedUserSlot data) external returns (Shares) {
        return Shares.wrap(uint112(PackedUserSlot.unwrap(data) & SHARES_MASK));
    }

    function interestRateHarness() external returns (uint72) {
        return vaultStorage.interestRate;
    }

    


     

}