import "./Base/liquidation.spec";




// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants: lastAccountStatusCheck <= block.timestamp

//------------------------------- RULES TEST START ----------------------------------

    //checkLiquidation works
    rule checkLiquidationIntegraty(env e) {
        //FUNCTION PARAMETER
        address liquidator;
        address violator;
        address collateral;
        //calculated values
        address liquidatorCalculated;
        address violatorCalculated;
        address collateralCalculated;
        address[] collateralsCalculated;
        LiquidationHarness.Assets liabilityCalculated;
        LiquidationHarness.Assets repayCalculated;
        uint256 yieldBalanceCalculated;
    
        LiquidationHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        liquidatorCalculated,violatorCalculated,collateralCalculated,collateralsCalculated,liabilityCalculated,repayCalculated,yieldBalanceCalculated = getCurrentLiquidationCacheHarness(e,vaultCache, liquidator, violator, collateral, max_uint256);

        //VALUES BEFORE

        //FUNCTION CALL
        uint256 repayCall;
        uint256 yieldBalanceCall;
        (repayCall, yieldBalanceCall) = checkLiquidation(e, liquidator, violator, collateral);

        //VALUES AFTER

        //ASSERTS
        //assert1: repayCall and yieldBalanceCall are the same as in the calculated liquidation cache
        assert(to_mathint(repayCalculated) == to_mathint(repayCall) && yieldBalanceCalculated == yieldBalanceCall, "Repay and yieldBalance are not the same as in the calculated liquidation cache");
    }


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------
//



    //checkLiquidation reverts
    rule checkLiquidationReverts(env e) {
        //FUNCTION PARAMETER
        address liquidator;
        address violator;
        address collateral;
        LiquidationHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        bool isRecognizedCollateral = isRecognizedCollateralExt(collateral);
        bool isCollateralEnabled = isCollateralEnabledExt(violator, collateral);
        bool isAccountStatusCheckDeferred = isAccountStatusCheckDeferredExt(violator);
        bool isInLiquidationCoolOff = isInLiquidationCoolOffExt(e, violator);


        //VALUES BEFORE

        //FUNCTION CALL
        checkLiquidation@withrevert(e, liquidator, violator, collateral);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert1: if liquidator and violator are the same, the function reverts
        assert(liquidator == violator => reverted, "Liquidator and violator are the same, but the function did not revert");

        //assert2: if collateral is not recognized, the function reverts
        assert(!isRecognizedCollateral => reverted, "Collateral is not recognized, but the function did not revert");	

        //assert3: if collateral is not enabled, the function reverts
        assert(!isCollateralEnabled => reverted, "Collateral is not enabled, but the function did not revert");

        //assert4: if account status check is deferred, the function reverts
        assert(isAccountStatusCheckDeferred => reverted, "Account status check is deferred, but the function did not revert");

        //assert5: if violator is in liquidation cool off, the function reverts
        assert(isInLiquidationCoolOff => reverted, "Violator is in liquidation cool off, but the function did not revert");

    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
