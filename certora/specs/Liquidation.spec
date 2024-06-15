import "./Base/liquidation.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as Collateral;
using LiquidationHarness as LiquidationHarness;




// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants: lastAccountStatusCheck <= block.timestamp
// when liquidating, the amount of debt should stay the same between the liquidator and the violator

//------------------------------- RULES TEST START ----------------------------------

















    //liquidate reverts
    rule liquidateReverts(env e) {
        //FUNCTION PARAMETER
        address violator;
        address collateral; 
        uint256 repayAssets; 
        uint256 minYieldBalance;

        //VALUES BEFORE
        address liquidator = actualCaller(e); //i: onBehalfOf
        bool controllerEnabled = vaultIsController(liquidator);
        bool isRecognizedCollateral = isRecognizedCollateralExt(collateral);
        bool isCollateralEnabled = isCollateralEnabledExt(violator, collateral);
        bool isAccountStatusCheckDeferred = isAccountStatusCheckDeferredExt(violator);
        bool isInLiquidationCoolOff = isInLiquidationCoolOffExt(e, violator);
        address[] collaterals = getCollateralsExt(violator);
        address[] controlers = getControlersExt(violator);
        LiquidationHarness.VaultCache vaultCache = CVLUpdateVault();
        LiquidationHarness.Assets liability = owedToAssetsUpHarness(owedGhost[violator]);
        LiquidationHarness.Assets repayCalculated;
        uint256 yieldBalanceCalculated;
        repayCalculated, yieldBalanceCalculated = calculateMaxLiquidationHarness(e, vaultCache, violator, collateral, collaterals, liability, 0,0);
        uint256 collateralBalanceViolater = Collateral.balanceOf(e, violator);
        uint256 collateralValue = getValueCollateralExt(e, collateralBalanceViolater, collateral, vaultCache.oracle, vaultCache.unitOfAccount);
        //CAPED VALUES
        mathint yieldBalanceCapped; 
        if(repayAssets != max_uint256 && repayCalculated != 0){
            yieldBalanceCapped = repayAssets * yieldBalanceCalculated / repayCalculated;
        } else{
            yieldBalanceCapped = 0;
        }
        mathint finalYieldBalance = 
        liability == 0 ? 0 : //i: return before calculateMaxLiquidation 
        repayAssets != max_uint256 && yieldBalanceCalculated > 0 ? yieldBalanceCapped //i: dont want to repay all and there is something to repay
        : yieldBalanceCalculated; //i: want to repay all or there is nothing to repay



        //FUNCTION CALL
        liquidate@withrevert(e, violator, collateral, repayAssets, minYieldBalance);
        bool reverted = lastReverted;
        //VALUES AFTER

        //ASSERTS


        //assert9: if the desired repay is higher than the calculated repay, the function reverts//@audit time out
        assert(liability != 0 && repayAssets != max_uint256 && to_mathint(repayAssets) > to_mathint(repayCalculated) => reverted, "Desired repay is higher than the calculated repay, but the function did not revert");




        // //assert12: minYieldBalance > finalYieldBalance, the function reverts //@audit does not work, check why: CollateralValue != 0
        // assert(liability != 0 && collateralValue != 0 && yieldBalanceCalculated > 0 && to_mathint(minYieldBalance) > finalYieldBalance => reverted, "minYieldBalance is higher than the finalYieldBalance, but the function did not revert");

        // //assert13: if the amount that should be repayed is bigger than the fromOwed, the function reverts

        //------------------ASSERTS OK START------------------   
            // //assert1: if liquidator and violator are the same, the function reverts
            // assert(liquidator == violator => reverted, "Liquidator and violator are the same, but the function did not revert");

            // //assert2: if collateral is not recognized, the function reverts
            // assert(!isRecognizedCollateral => reverted, "Collateral is not recognized, but the function did not revert");	

            // //assert3: if collateral is not enabled, the function reverts
            // assert(!isCollateralEnabled => reverted, "Collateral is not enabled, but the function did not revert");

            // //assert4: if account status check is deferred, the function reverts
            // assert(isAccountStatusCheckDeferred => reverted, "Account status check is deferred, but the function did not revert");

            // //assert5: if violator is in liquidation cool off, the function reverts
            // assert(isInLiquidationCoolOff => reverted, "Violator is in liquidation cool off, but the function did not revert");

            // // assert6: if controllers.length > 1, the function reverts
            // assert(controlers.length > 1 => reverted, "There are more than one controller, but the function did not revert");

            // //assert7: if controllers.length == 0, the function reverts
            // assert(controlers.length == 0 => reverted, "There are no controllers, but the function did not revert");

            // //assert8: if controllers[0] != currentContract, the function reverts
            // assert(controlers[0] != currentContract => reverted, "The controller is not the current contract, but the function did not revert");

            
            
            // //assert10: if e.msg.sender is not EVC, the function reverts
            // assert(e.msg.sender != EVC => reverted, "e.msg.sender is not EVC, but the function did not revert");

            // //assert11: if !controllerEnabled, the function reverts
            // assert(!controllerEnabled => reverted, "Controller is not enabled, but the function did not revert");



        //------------------ASSERTS OK END------------------

    }

    //liquidate works
    rule liquidateIntegraty(env e){
        //FUNCTION PARAMETER
        address violator;
        address collateral;
        require(collateral == Collateral);
        uint256 repayAssets;
        uint256 minYieldBalance;
        //USERS
        address liquidator = actualCaller(e);
        address otherUser;
        require(otherUser != violator && otherUser != liquidator);

        //BALANCES BEFORE
        Type.Owed owedViolatorBefore = owedGhost[violator];
        Type.Owed owedLiquidatorBefore = owedGhost[liquidator];
        Type.Owed owedOtherUserBefore = owedGhost[otherUser];
        uint256 balanceCollateralViolatorBefore = collateralBalancesGhost[violator];
        uint256 balanceCollateralLiquidatorBefore = collateralBalancesGhost[liquidator];
        uint256 balanceCollateralOtherUserBefore = collateralBalancesGhost[otherUser];

        //VALUES BEFORE
        LiquidationHarness.VaultCache vaultCache = CVLUpdateVault();
        Type.Owed totalBorrowBefore = vaultCache.totalBorrows;
        address[] collaterals = getCollateralsExt(violator);
        // bool liquidationHappens //@audit owedViolatorBefore

        //FINAL VALUES
        Type.Assets owedViolatorBeforeAsAssets = owedToAssetsUpHarness(owedViolatorBefore);
        Type.Assets repayCalculated;
        uint256 yieldBalanceCalculated;
        repayCalculated, yieldBalanceCalculated = calculateMaxLiquidationHarness(e, vaultCache, violator, collateral, collaterals, owedViolatorBeforeAsAssets, 0,0);
        require(repayAssets == max_uint256 || to_mathint(repayAssets) <= to_mathint(repayCalculated));
        //finalRepay
        Type.Assets finalRepay;
        if(owedViolatorBefore == 0){ //if owedViolatorBefore = 0 => finalRepay = 0
                finalRepay = 0;
            } else if(repayAssets == max_uint256){//repayAssets == max_uint256 => finalRepay = repayCalculated
                finalRepay = repayCalculated;
            }else if(repayCalculated == 0){ //repayAssets != max_uint256 && repayCalculated = 0 => finalRepay = repayCalculated = 0;
                finalRepay = repayCalculated;
            } else{ //repayAssets != max_uint256 && repayCalculated > 0 => finalRepay = repayAssets.toAssets();
                finalRepay = uintToAssetsHarness(repayAssets);
        }

        //finalYieldBalance
        uint256 finalYieldBalance;
        if(owedViolatorBefore == 0){ //if owedViolatorBefore = 0 => finalRepay = 0
                finalYieldBalance = 0;
            } else if(repayAssets == max_uint256){//repayAssets == max_uint256 => finalYieldBalance = yieldBalanceCalculated
                finalYieldBalance = yieldBalanceCalculated;
            }else if(repayCalculated == 0){ //repayAssets != max_uint256 && repayCalculated = 0 => finalYieldBalance = yieldBalanceCalculated
                finalYieldBalance = yieldBalanceCalculated;
            } else{ //repayAssets != max_uint256 && repayCalculated > 0 => finalYieldBalance = repayAssets * yieldBalanceCalculated / repayCalculated;
                finalYieldBalance = assert_uint256(repayAssets * yieldBalanceCalculated / repayCalculated);
        }

        //FUNCTION CALL
        liquidate(e, violator, collateral, repayAssets, minYieldBalance);

        //VALUES AFTER
        LiquidationHarness.VaultCache vaultCacheAfter = CVLUpdateVault();
        Type.Owed totalBorrowAfter = vaultCacheAfter.totalBorrows;
        Type.Owed owedViolatorAfter = owedGhost[violator];
        Type.Owed owedLiquidatorAfter = owedGhost[liquidator];
        Type.Owed owedOtherUserAfter = owedGhost[otherUser];
        uint256 balanceCollateralViolatorAfter = collateralBalancesGhost[violator];
        uint256 balanceCollateralLiquidatorAfter = collateralBalancesGhost[liquidator];
        uint256 balanceCollateralOtherUserAfter = collateralBalancesGhost[otherUser];
        //should remainig debt be socialized
        bool hasNoCollateral = checkNoCollateralHarness(violator, collaterals);
        bool socializeDebt = socializeDebtHarness(vaultCache.configFlags);
        bool notAllRepayed = to_mathint(owedViolatorBefore) > to_mathint(finalRepay);
        bool adjustOwedRemainingViolator = hasNoCollateral && notAllRepayed && socializeDebt;
        mathint remainingOwedViolator = owedViolatorBefore - assetsToOwedHarness(finalRepay);




        //ASSERTS
        // //assert1: if violator still has collateral owed of violator is decreased by repayAssets
        // assert(!adjustOwedRemainingViolator => to_mathint(owedViolatorAfter) == owedViolatorBefore - finalRepay, "Owed of violator has not decreased by repayAssets");

        // //assert2: owed of liquidator is increased by repayAssets
        // assert(to_mathint(owedLiquidatorAfter) == owedLiquidatorBefore + finalRepay, "Owed of liquidator has not increased by repayAssets");

        // //assert4: the collateral of violator is decreased by the value of the collateral
        // assert(to_mathint(balanceCollateralViolatorAfter) == balanceCollateralViolatorBefore - finalYieldBalance, "Collateral of violator has not decreased by the value of the collateral");

        // //assert5: the collateral of liquidator is increased by the value of the collateral
        // assert(to_mathint(balanceCollateralLiquidatorAfter) == balanceCollateralLiquidatorBefore + finalYieldBalance, "Collateral of liquidator has not increased by the value of the collateral");

        //assert7: if noMoreCollateral, totalBorrow is reduced by owedRemaining
        assert(owedViolatorBefore != 0 && adjustOwedRemainingViolator => to_mathint(totalBorrowAfter) == totalBorrowBefore - remainingOwedViolator, "Total borrow is not reduced by owedRemaining"); //@audit might fail because of types Owed and Assets mixed



        //-------------------------- ASSERTS OK START --------------------------


            // //assert3: owed of otherUser has not changed
            // assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of otherUser has changed");



            // //assert6: the collateral of otherUser has not changed
            // assert(balanceCollateralOtherUserBefore == balanceCollateralOtherUserAfter, "Collateral of otherUser has changed");


            // //assert8: if noMoreCollateral, owedViolatorAfter is 0
            // assert(adjustOwedRemainingViolator => owedViolatorAfter == 0, "Owed of violator is not 0");



        //-------------------------- ASSERTS OK END --------------------------


    }



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------
//

    //only changes owed
    rule onlyChangesOwed(env e, method f, calldataarg args) filtered{
        f-> !BASE_HARNESS_FUNCTIONS(f) && !f.isView && !f.isPure
    }{
        //VALUES BEFORE
        address account;
        Type.Owed owedBefore = owedGhost[account];

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = owedGhost[account];

        //ASSERTS
        assert(owedBefore != owedAfter =>
        f.selector == sig:liquidate(address,address,uint256,uint256).selector, "Owed has not changed correctly");
    }

    //only changes totalBorrows
    rule onlyChangesTotalBorrows(env e, method f, calldataarg args) filtered{
        f-> !BASE_HARNESS_FUNCTIONS(f) && !f.isView && !f.isPure
    }{
        //VALUES BEFORE
        LiquidationHarness.VaultCache vaultCache = CVLUpdateVault();
        Type.Owed totalBorrowBefore = vaultCache.totalBorrows;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        LiquidationHarness.VaultCache vaultCacheAfter = CVLUpdateVault();
        Type.Owed totalBorrowAfter = vaultCacheAfter.totalBorrows;

        //ASSERTS
        assert(totalBorrowBefore != totalBorrowAfter =>
        f.selector == sig:liquidate(address,address,uint256,uint256).selector, "Total borrows has not changed correctly");
    }

    //only changes userInterestAccumulator
    rule onlyChangesUserInterestAccumulator(env e, method f, calldataarg args) filtered{
        f-> !BASE_HARNESS_FUNCTIONS(f) && !f.isView && !f.isPure
    }{
        //VALUES BEFORE
        address account;
        uint256 interestAccumulatorBefore = interestAccumulatorsGhost[account];

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 interestAccumulatorAfter = interestAccumulatorsGhost[account];

        //ASSERTS
        assert(interestAccumulatorBefore != interestAccumulatorAfter =>
        f.selector == sig:liquidate(address,address,uint256,uint256).selector, "Interest accumulator has not changed correctly");
    }

    //only changes collateral balances
    rule onlyChangesCollateralBalances(env e, method f, calldataarg args) filtered{
        f-> !BASE_HARNESS_FUNCTIONS(f) && !f.isView && !f.isPure
    }{
        //VALUES BEFORE
        address account;
        require(getAssetHarness(e) == Collateral);
        uint256 balanceBefore = Collateral.balanceOf(e, account);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 balanceAfter = Collateral.balanceOf(e, account);

        //ASSERTS
        assert(balanceBefore != balanceAfter =>
        f.selector == sig:liquidate(address,address,uint256,uint256).selector, "Collateral balance has not changed correctly");
    }

    //nonReentrantView modifier works
    rule nonReentrantViewWorks(env e, method f, calldataarg args) filtered{
        f-> NONREENTRANTVIEW_FUNCTIONS(f)
    }{
        //VALUES BEFORE
        bool reentrancyLocked = LiquidationHarness.vaultStorage.reentrancyLocked;
        address hookTarget = LiquidationHarness.vaultStorage.hookTarget;
        bool shouldRevert = e.msg.sender != hookTarget && !(e.msg.sender == currentContract && CVLUseViewCaller() == hookTarget);

        //FUNCTION CALL
        f@withrevert(e, args);
        bool reverted = lastReverted;

        //ASSERTS
        assert(reentrancyLocked && shouldRevert => reverted, "Function call should revert");
    }

    //nonReentrant modifier works
    rule nonReentrantWorks(env e, method f, calldataarg args) filtered{
        f-> NONREENTRANT_FUNCTIONS(f)
    }{
        //VALUES BEFORE
        bool reentrancyLocked = LiquidationHarness.vaultStorage.reentrancyLocked;

        //FUNCTION CALL
        f@withrevert(e, args);

        //ASSERTS
        assert(reentrancyLocked => lastReverted, "Function call should revert");

    }

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
        address[] controlers = getControlersExt(violator);


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

        //assert6: if controllers.length > 1, the function reverts
        assert(controlers.length > 1 => reverted, "There are more than one controller, but the function did not revert");

        //assert7: if controllers.length == 0, the function reverts
        assert(controlers.length == 0 => reverted, "There are no controllers, but the function did not revert");

        //assert8: if controllers[0] != currentContract, the function reverts
        assert(controlers[0] != currentContract => reverted, "The controller is not the current contract, but the function did not revert");

    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
