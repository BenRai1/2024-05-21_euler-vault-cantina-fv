import "./Base/liquidation_short.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as Collateral;
using LiquidationHarness as LiquidationHarness;




// used to test running time
use builtin rule sanity;
// use rule privileg0edOperation;



//------------------------------- RULES OK START ------------------------------------


    //calculateLiquidation works
    rule calculateLiquidationIntegraty(env e) {
        //FUNCTION PARAMETER
        LiquidationHarness.VaultCache vaultCache;
        address liquidator;
        address violator;
        address collateral;
        uint256 desiredRepay;
        bool isRecognizedCollateral = isRecognizedCollateralExt(collateral);
        bool isCollateralEnabled = isCollateralEnabledExt(violator, collateral);
        bool isAccountStatusCheckDeferred = isAccountStatusCheckDeferredExt(violator);
        bool isInLiquidationCoolOff = isInLiquidationCoolOffExt(e, violator);
        //VALUES CALCULATED
        LiquidationHarness.Assets liability = getCurrentOwedExt(e, vaultCache, violator);
        address[] collaterals = getCollateralsExt(violator);

        LiquidationHarness.Assets repayCalculated;
        uint256 yieldBalanceCalculated;
        repayCalculated, yieldBalanceCalculated = calculateMaxLiquidationHarness(e, vaultCache, violator, collateral, collaterals, liability, 0,0);

        //CAPED VALUES
        mathint yieldBalanceCapped; 
        if(repayCalculated != 0){
            yieldBalanceCapped = desiredRepay * yieldBalanceCalculated / repayCalculated;
        } else{
            yieldBalanceCapped = 0;
        }

        //FUNCTION CALL
        address liquidatorCall;
        address violatorCall;
        address collateralCall;
        address[] collateralsCall;
        LiquidationHarness.Assets liabilityCall;
        LiquidationHarness.Assets repayCall;
        uint256 yieldBalanceCall;
        liquidatorCall,violatorCall,collateralCall,collateralsCall,liabilityCall,repayCall,yieldBalanceCall  = calculateLiquidationExt(e, vaultCache,liquidator, violator, collateral, desiredRepay);

        // ASSERTS
        //assert1: if liabilities are 0, the returnValues are 0
        assert(liability == 0 => repayCall == 0 && yieldBalanceCall == 0, "Liabilities are 0, but the return values are not 0");

        //assert2: if liabilities are not 0 and desiredRepay == max_uint256, the returnValues are the same as in the calculated values
        assert(liability != 0 && desiredRepay == max_uint256 => to_mathint(repayCalculated) == to_mathint(repayCall) && yieldBalanceCalculated == yieldBalanceCall, "Liabilities are not 0 and desiredRepay == max_uint256, but the return values are not the same as in the calculated values");

        //assert3: if liabilities are not 0 and desiredRepay != max_uint256 and repay > 0, the returnValues are the same as in the caped values 
        assert(liability != 0 && desiredRepay != max_uint256 && to_mathint(repayCalculated) > 0 => to_mathint(desiredRepay) == to_mathint(repayCall) && yieldBalanceCapped == to_mathint(yieldBalanceCall), "Liabilities are not 0 and desiredRepay != max_uint256 and repay > 0, but the return values are not the same as in the caped values");
    }

    //calculateLiquidation reverts
    rule calculateLiquidationReverts(env e) {
        //FUNCTION PARAMETER
        LiquidationHarness.VaultCache vaultCache;
        address liquidator;
        address violator;
        address collateral;
        uint256 desiredRepay;
        bool isRecognizedCollateral = isRecognizedCollateralExt(collateral);
        bool isCollateralEnabled = isCollateralEnabledExt(violator, collateral);
        bool isAccountStatusCheckDeferred = isAccountStatusCheckDeferredExt(violator);
        bool isInLiquidationCoolOff = isInLiquidationCoolOffExt(e, violator);
        //VALUES CALCULATED
        LiquidationHarness.Assets liability = getCurrentOwedExt(e, vaultCache, violator);
        address[] collaterals = getCollateralsExt(violator);
        address[] controlers = getControlersExt(violator);

        LiquidationHarness.Assets repayCalculated;
        uint256 yieldBalanceCalculated;
        repayCalculated, yieldBalanceCalculated = calculateMaxLiquidationHarness(e, vaultCache, violator, collateral, collaterals, liability, 0,0);

        //FUNCTION CALL
        calculateLiquidationExt@withrevert(e, vaultCache, liquidator, violator,collateral, desiredRepay);
        bool reverted = lastReverted;

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

        // assert6: if controllers.length > 1, the function reverts
        assert(controlers.length > 1 => reverted, "There are more than one controller, but the function did not revert");

        //assert7: if controllers.length == 0, the function reverts
        assert(controlers.length == 0 => reverted, "There are no controllers, but the function did not revert");

        //assert8: if controllers[0] != currentContract, the function reverts
        assert(controlers[0] != currentContract => reverted, "The controller is not the current contract, but the function did not revert");

        //assert9: if the desired repay is higher than the calculated repay, the function reverts
        assert(liability != 0 && desiredRepay != max_uint256 && to_mathint(desiredRepay) > to_mathint(repayCalculated) => reverted, "Desired repay is higher than the calculated repay, but the function did not revert");
    }

    
//------------------------------- RULES OK END ------------------------------------

