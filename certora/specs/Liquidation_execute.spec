import "./Base/liquidation.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as Collateral;




// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//zusammenfassen von     function calculateMaxLiquidation(
//=> ghost variables for 
//=> 

//summ up getCollaterals (limit collaterals to 1)
methods {

    function _.calculateLiquidation(
        Type.VaultCache memory vaultCache,
        address liquidator,
        address violator,
        address collateral,
        uint256 desiredRepay
    // certora: 'private' to 'internal'
    ) internal => CVLCalculateLiquidation(liquidator, violator, collateral, desiredRepay) expect (Type.LiquidationCache memory); 

}

function CVLCalculateLiquidation(
    address liquidator,
    address violator,
    address collateral,
    uint256 desiredRepay
) returns Type.LiquidationCache {
    Type.LiquidationCache cache;
    require(cache.liquidator == liquidator);
    require(cache.violator == violator);
    require(cache.collateral == collateral);
    require(cache.collaterals.length == 1);
    require(cache.collaterals[0] == collateralsGhost[violator]);
    
    Type.Assets liability = owedToAssetsUpHarness(owedGhost[violator]);
    require(cache.liability == liability);
    Type.Assets repay = repayGhost[liquidator];
    require(cache.repay == repay);
    uint256 yieldBalance = yieldBalanceGhost[liquidator];
    require(cache.yieldBalance == yieldBalance);

    return cache;    
}

ghost mapping(address => address) collateralsGhost;

ghost mapping(address => Type.Assets) repayGhost;

ghost mapping(address => uint256) yieldBalanceGhost;

function CVLGetCollaterals(address account) returns address[] {
    address[] collaterals;
    require(collaterals.length == 1);
    require(collaterals[0] == collateralsGhost[account]);
    return collaterals;
}   


//------------------------------- RULES TEST START ----------------------------------

// //executeLiquidation reverts
// rule executeLiquidationReverts(env e){ //@audit-check this should be ok to fix
//     //FUNCTION PARAMETER
//     address violator;
//     address collateral;
//     uint256 repayAssets;
//     uint256 minYieldBalance;

//     address liquidator = actualCaller(e); //i: onBehalfOf
//     Type.VaultCache vaultCache = CVLUpdateVault();
//     Type.LiquidationCache liquidationCache = CVLCalculateLiquidation(liquidator, violator, collateral, repayAssets);

//     //VALUES BEFORE
//     Type.Owed owedViolatorBefore = owedGhost[violator];
//     Type.Owed repayAsOwed = assetsToOwedHarness(liquidationCache.repay); //i: amount
//     Type.Owed finalAmount = finalAmountDustHarness(repayAsOwed, owedViolatorBefore);
//     bool isLiquidationDisabled = isLiquidationDisabled();

//     //FUNCTION CALL
//     liquidate@withrevert(e, violator, collateral, repayAssets, minYieldBalance);
//     //must call liquidate, calculateLiquidation is summarized

//     //VALUES AFTER

//     //ASSERTS
//     // //assert1: if minYealdBalance > yieldBalance, the function reverts
//     // assert(minYieldBalance > liquidationCache.yieldBalance => lastReverted, "minYieldBalance is higher than yieldBalance, but the function did not revert");

//     //assert2: if the finalAmount that should be repayed is bigger than the owedViolatorBefore, the function reverts
//     // assert(finalAmount > owedViolatorBefore => lastReverted, "FinalAmount is higher than owedViolatorBefore, but the function did not revert");


//     //assert3: if the owed remaining is bigger than the owed exact the function reverts

//     //assert4: if the liquidation is disabled, the function reverts
//     // assert(isLiquidationDisabled => lastReverted, "Liquidation is disabled, but the function did not revert");

   


// }



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------
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

        // bool isLiquidationDisabled = isLiquidationDisabled();



        //FUNCTION CALL
        liquidate@withrevert(e, violator, collateral, repayAssets, minYieldBalance);
        bool reverted = lastReverted;
        //VALUES AFTER

        //ASSERTS


        //assert9: if the desired repay is higher than the calculated repay, the function reverts//@audit time out
        // assert(liability != 0 && repayAssets != max_uint256 && to_mathint(repayAssets) > to_mathint(repayCalculated) => reverted, "Desired repay is higher than the calculated repay, but the function did not revert");




        // //assert12: minYieldBalance > finalYieldBalance, the function reverts //@audit does not work, check why: CollateralValue != 0
        // assert(liability != 0 && collateralValue != 0 && yieldBalanceCalculated > 0 && to_mathint(minYieldBalance) > finalYieldBalance => reverted, "minYieldBalance is higher than the finalYieldBalance, but the function did not revert");

        // //assert13: if the amount that should be repayed is bigger than the fromOwed, the function reverts

        //------------------ASSERTS OK START------------------   
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

            
            
            //assert10: if e.msg.sender is not EVC, the function reverts
            assert(e.msg.sender != EVC => reverted, "e.msg.sender is not EVC, but the function did not revert");

            //assert11: if !controllerEnabled, the function reverts
            assert(!controllerEnabled => reverted, "Controller is not enabled, but the function did not revert");

            //assert14: if the liquidation is disabled, the function reverts
            // assert(isLiquidationDisabled => reverted, "Liquidation is disabled, but the function did not revert");



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

        // //assert7: if noMoreCollateral, totalBorrow is reduced by owedRemaining
        // assert(owedViolatorBefore != 0 && adjustOwedRemainingViolator => to_mathint(totalBorrowAfter) == totalBorrowBefore - remainingOwedViolator, "Total borrow is not reduced by owedRemaining"); //@audit might fail because of types Owed and Assets mixed



        //-------------------------- ASSERTS OK START --------------------------


            //assert3: owed of otherUser has not changed
            assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of otherUser has changed");



            //assert6: the collateral of otherUser has not changed
            assert(balanceCollateralOtherUserBefore == balanceCollateralOtherUserAfter, "Collateral of otherUser has changed");


            //assert8: if noMoreCollateral, owedViolatorAfter is 0
            assert(adjustOwedRemainingViolator => owedViolatorAfter == 0, "Owed of violator is not 0");



        //-------------------------- ASSERTS OK END --------------------------


    }

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------


//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
