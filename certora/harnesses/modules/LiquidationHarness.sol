// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;
import "../../../src/interfaces/IPriceOracle.sol";
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Liquidation.sol";
// import "../AbstractBaseHarness.sol";

contract LiquidationHarness is AbstractBaseHarness, Liquidation {
    uint32 constant CFG_DONT_SOCIALIZE_DEBT = 1 << 0;


    using TypesLib for uint16;
    using TypesLib for uint256;
    constructor(Integrations memory integrations) Liquidation(integrations) {}

    function calculateLiquidityExternal(
        address account
    ) public view returns (uint256 collateralValue, uint256 liabilityValue) {
        return calculateLiquidity(loadVault(), account, getCollaterals(account), true);
    }

    function calculateLiquidationExt(
        VaultCache memory vaultCache,
        address liquidator,
        address violator,
        address collateral,
        uint256 desiredRepay
    ) external view returns (        
            address liquidatorRetunr,
            address violatorReturn,
            address collateralReturn,
            address[] memory collaterals,
            Assets liability,
            Assets repay,
            uint256 yieldBalance
    ) {
        LiquidationCache memory liquidationCache = calculateLiquidation(vaultCache, liquidator, violator, collateral, desiredRepay);
        liquidatorRetunr = liquidationCache.liquidator;
        violatorReturn = liquidationCache.violator;
        collateralReturn = liquidationCache.collateral;
        collaterals = liquidationCache.collaterals;
        liability = liquidationCache.liability;
        repay = liquidationCache.repay;
        yieldBalance = liquidationCache.yieldBalance;
    }

    function isRecognizedCollateralExt(address collateral) external view virtual returns (bool) {
        return isRecognizedCollateral(collateral);
    }

    function getLiquidator() external returns (address liquidator) {
        (, liquidator) = initOperation(OP_LIQUIDATE, CHECKACCOUNT_CALLER);
    }

    function getCurrentOwedExt(VaultCache memory vaultCache, address violator) external view returns (Assets) {
        return getCurrentOwed(vaultCache, violator).toAssetsUp();
    }

    function getCollateralValueExt(VaultCache memory vaultCache, address account, address collateral, bool liquidation)
        external
        view
        returns (uint256 value) {
            return getCollateralValue(vaultCache, account, collateral, liquidation);
    }

    function getCurrentLiquidationCacheHarness(
        VaultCache memory vaultCache,
        address liquidator,
        address violator,
        address collateral,
        uint256 desiredRepay)
        external returns (
            address liquidatorReturn,
            address violatorReturn,
            address collateralReturn,
            address[] memory collaterals,
            Assets liability,
            Assets repay,
            uint256 yieldBalance
        ) {
            liquidatorReturn = liquidator;
            violatorReturn = violator;
            collateralReturn = collateral;
            collaterals = getCollaterals(violator);
            liability = getCurrentOwed(vaultCache, violator).toAssetsUp();
            repay = Assets.wrap(0); //i: 0
            yieldBalance = 0;

            // Violator has no liabilities, liquidation is a no-op
            if (liability.isZero()) return (liquidator, violator, collateral, collaterals, liability, repay, yieldBalance);

            // Calculate max yield and repay
            (uint256 collateralAdjustedValue, uint256 liabilityValue) =
                calculateLiquidity(vaultCache, violator, collaterals, true);
            // no violation
            if (collateralAdjustedValue > liabilityValue) return (liquidator, violator, collateral, collaterals, liability, repay, yieldBalance);

            uint256 discountFactor = collateralAdjustedValue * 1e18 / liabilityValue; // discountFactor = health score = 1 - discount
            {
                uint256 minDiscountFactor;
                unchecked {
                    // discount <= config scale, so discount factor >= 0
                    minDiscountFactor = 1e18 - uint256(1e18) * vaultStorage.maxLiquidationDiscount.toUint16() / CONFIG_SCALE;
                }
                if (discountFactor < minDiscountFactor) discountFactor = minDiscountFactor;
            }

            // Compute maximum yield using mid-point prices

            uint256 collateralBalance = IERC20(collateral).balanceOf(violator);
            uint256 collateralValue =
                vaultCache.oracle.getQuote(collateralBalance, collateral, vaultCache.unitOfAccount);

            if (collateralValue == 0) {
                yieldBalance = collateralBalance;
                return  (liquidator, violator, collateral, collaterals, liability, repay, yieldBalance);
            }

            uint256 maxRepayValue = liabilityValue;
            uint256 maxYieldValue = maxRepayValue * 1e18 / discountFactor;

            if (collateralValue < maxYieldValue) {
                maxRepayValue = collateralValue * discountFactor / 1e18;
                maxYieldValue = collateralValue;
            }

            repay = (maxRepayValue * liability.toUint() / liabilityValue).toAssets();
            yieldBalance = maxYieldValue * collateralBalance / collateralValue;

            // Adjust for desired repay

            if (desiredRepay != type(uint256).max) {
                uint256 maxRepay = repay.toUint();
                if (desiredRepay > maxRepay) revert E_ExcessiveRepayAmount();

                if (maxRepay > 0) {
                    yieldBalance = desiredRepay * yieldBalance / maxRepay;
                    repay = desiredRepay.toAssets();
                }
            }
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
        vaultCache.snapshotInitialized = vaultStorage.snapshotInitialized;
        vaultCache.accumulatedFees = vaultStorage.accumulatedFees;
        vaultCache.configFlags = vaultStorage.configFlags;
        vaultCache.interestAccumulator = vaultStorage.interestAccumulator;
        return vaultCache;
    }

    function calculateMaxLiquidationHarness(
        VaultCache memory vaultCache,
        address violator,
        address collateral,
        address[] memory collaterals,
        Assets liability,
        Assets repay,
        uint256 yieldBalance
    )
        external
        view
        returns (Assets, uint256 )
    {
        // Check account health

        (uint256 collateralAdjustedValue, uint256 liabilityValue) =
            calculateLiquidity(vaultCache, violator, collaterals, true);

        // no violation
        if (collateralAdjustedValue > liabilityValue) return (repay,yieldBalance);

        // Compute discount

        uint256 discountFactor = collateralAdjustedValue * 1e18 / liabilityValue; // discountFactor = health score = 1 - discount
        {
            uint256 minDiscountFactor;
            unchecked {
                // discount <= config scale, so discount factor >= 0
                minDiscountFactor = 1e18 - uint256(1e18) * vaultStorage.maxLiquidationDiscount.toUint16() / CONFIG_SCALE;
            }
            if (discountFactor < minDiscountFactor) discountFactor = minDiscountFactor;
        }

        // Compute maximum yield using mid-point prices

        uint256 collateralBalance = IERC20(collateral).balanceOf(violator);
        uint256 collateralValue =
            vaultCache.oracle.getQuote(collateralBalance, collateral, vaultCache.unitOfAccount);

        if (collateralValue == 0) {
            yieldBalance = collateralBalance;
            return (repay, yieldBalance);
        }

        uint256 maxRepayValue = liabilityValue;
        uint256 maxYieldValue = maxRepayValue * 1e18 / discountFactor;

        if (collateralValue < maxYieldValue) {
            maxRepayValue = collateralValue * discountFactor / 1e18;
            maxYieldValue = collateralValue;
        }

        repay = (maxRepayValue * liability.toUint() / liabilityValue).toAssets();
        yieldBalance = maxYieldValue * collateralBalance / collateralValue;

        return (repay, yieldBalance);
    }

    function getValueCollateralExt(uint256 collateralBalance, address collateral, address oracle, address unitOfAccount) external view returns (uint256) {
        return IPriceOracle(collateral).getQuote(collateralBalance, collateral, unitOfAccount);
    }

    function checkNoCollateralHarness(address account, address[] memory collaterals) external view returns (bool) {
        return checkNoCollateral(account, collaterals);
    }

    function socializeDebtHarness(Flags configFlags) external returns(bool){
        return configFlags.isNotSet(CFG_DONT_SOCIALIZE_DEBT);
    }


    function finalAmountDustHarness(Owed amount, Owed currentOwed) external pure returns (Owed) {
        if (
            (amount > currentOwed && amount.subUnchecked(currentOwed).isDust())
                || (amount < currentOwed && currentOwed.subUnchecked(amount).isDust())
        ) {
            return currentOwed;
        } 
        return amount;  
    }

    function getAssetHarness() external view returns (address) {
        (IERC20 asset, ,) = ProxyUtils.metadata();
        return address(asset);
    }
}