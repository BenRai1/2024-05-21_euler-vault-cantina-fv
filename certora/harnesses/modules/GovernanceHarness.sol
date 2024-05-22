// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Governance.sol";
import {IIRM} from "../../../src/InterestRateModels/IIRM.sol";



contract GovernanceHarness is Governance, AbstractBaseHarness {
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

    function reentrancyLockedHarness() external returns (bool) {
        return vaultStorage.reentrancyLocked;
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
        return loadVault();
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

    


     

}