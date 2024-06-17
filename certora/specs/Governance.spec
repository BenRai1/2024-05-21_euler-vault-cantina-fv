import "./Base.spec";
import "./Base/governance.spec";
using MockHookTarget as HookTarget;
using ProtocolConfig as ProtocolConfig;
using GovernanceHarness as Governance;

// used to test running time
use builtin rule sanity;
// use rule privilegedOperation;

//suggestions for spec split
//1. onlyChange functions
//2. view functions

//invariants:
//- interstRate should never be bigger than MAX_ALLOWED_INTEREST_RATE
//- lastInterestAccumulatorUpdate should never be bigger than the current block timestamp
//- totalBorrowed should never be bigger than totalShares
//- borrowLTV should never be bigger than liquidationLTV

//------------------------------- RULES TEST START ----------------------------------

   














   






//------------------------------- TESTING ----------------------------------


//------------------------------- RULES TEST END ----------------------------------

// //------------------------------- RULES PROBLEMS START ----------------------------------


   


//     //only spesific functions should change balances //@audit setLTV also changes balances, check why
//     rule onlyChangeBalances(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
//         address user;
//         GovernanceHarness.PackedUserSlot userDataBefore = getUserStorageDataHarness(user);
//         GovernanceHarness.Shares sharesBefore = unpackBalanceHarness(userDataBefore);
        
//         f(e, args);

//         GovernanceHarness.PackedUserSlot userDataAfter = getUserStorageDataHarness(user);
//         GovernanceHarness.Shares sharesAfter = unpackBalanceHarness(userDataAfter);

//         assert(userDataBefore != userDataAfter =>
//         f.selector == sig:convertFees().selector, "Balances was changed by unothorised function");
//     }


//         // getting LTVLiquidation(address) works //@audit does not work
//     rule getLTVLiquidationIntegraty(env e) {
//         address collateral;
//         GovernanceHarness.LTVConfig ltvLookup = Governance.vaultStorage.ltvLookup[collateral];
//         uint16 liquidationLTV = getLTVTrueHarness(e, ltvLookup );

//         //function call
//         uint16 liquidationLTVCall = LTVLiquidation(e, collateral);

//         assert(liquidationLTVCall == liquidationLTV, "Liquidation LTV was not returned correctly");
//     }

//     // getting protocolFeeReceiver works //@audit does not work
//     rule getProtocolFeeReceiverIntegraty(env e) {
//         bool exist = ProtocolConfig._protocolFeeConfig[currentContract].exists;
//         address protocolFeeReceiver;
//         if(exist){
//             protocolFeeReceiver = ProtocolConfig._protocolFeeConfig[currentContract].feeReceiver;
//         }else{
//             protocolFeeReceiver = 0;
//         }

//         //function call
//         address protocolFeeReceiverCall = protocolFeeReceiver();

//         assert(protocolFeeReceiverCall == protocolFeeReceiver, "Protocol fee receiver was not returned correctly");
//     }

//     // getting protocolFeeShare works //@audit does not work
//     rule getProtocolFeeShareIntegraty(env e) {
//         bool exist = ProtocolConfig._protocolFeeConfig[currentContract].exists;
//         uint16 protocolFeeShare;
//         if(exist){
//             protocolFeeShare = ProtocolConfig._protocolFeeConfig[currentContract].protocolFeeShare;
//         } else {
//             protocolFeeShare = 0;
//         }

//         //function call
//         uint256 protocolFeeShareCall = protocolFeeShare();

//         assert(to_mathint(protocolFeeShareCall) == to_mathint(protocolFeeShare), "Protocol fee share was not returned correctly");
//     }



// //------------------------------- RULES PROBLEMS END ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    // //setLTV works //@audit-check worked and now does not work
    // rule setLTVIntegraty(env e) {
    //     address collateral;
    //     require(collateral != 0);
    //     uint16 borrowLTV;
    //     GovernanceHarness.ConfigAmount newBorrowLTV = toConfigAmountHarness(borrowLTV);
    //     uint16 liquidationLTV;
    //     GovernanceHarness.ConfigAmount newLiquidationLTV = toConfigAmountHarness(liquidationLTV);
    //     uint32 rampDuration;
    //     require(e.block.timestamp + rampDuration <=max_uint48);

    //     //VALUES BEFORE
    //     GovernanceHarness.LTVConfig ltvConfigBefore = getCurrentLTVConfigHarness(collateral); 
    //     bool isInitialized = ltvConfigBefore.initialized;
    //     GovernanceHarness.ConfigAmount currentTvlBefore = calculateLiquidationLTVHarness(e, ltvConfigBefore, true);
    //     uint256 nuberOfLTVsBefore = LTVList().length;

    //     //FUNCTION CALL
    //     setLTV(e, collateral, borrowLTV, liquidationLTV, rampDuration);

    //     //VALUES AFTER
    //     GovernanceHarness.LTVConfig LTVConfigAfter = getCurrentLTVConfigHarness(collateral);
    //     uint256 nuberOfLTVsAfter = LTVList().length;

    //     //ASSERTS
    //     //assert1: borrowLTVAfter = newBorrowLTV 
    //     assert(LTVConfigAfter.borrowLTV == newBorrowLTV, "Borrow LTV was not set correctly");

    //     //assert2: liquidationLTVAfter = liquidationLTV
    //     assert(LTVConfigAfter.liquidationLTV == newLiquidationLTV, "Liquidation LTV was not set correctly");

    //     //assert3: initialLiquidationLTVAfter = ???
    //     assert(LTVConfigAfter.initialLiquidationLTV == currentTvlBefore, "Initial liquidation LTV was not set correctly");

    //     //assert4: targetTimestampAfter = e.block.timestamp + rampDuration
    //     assert(LTVConfigAfter.targetTimestamp == assert_uint48(e.block.timestamp + rampDuration), "Target timestamp was not set correctly");

    //     //assert5: rampDurationAfter = rampDuration
    //     assert(LTVConfigAfter.rampDuration == rampDuration, "Ramp duration was not set correctly");

    //     //assert6: currentLtvConfigAfter.initialized = true
    //     assert(LTVConfigAfter.initialized == true, "Initialized was not set correctly");

        
    //     // //assert7: if !initailized, the LTV is added to the LTVList
    //     assert(!isInitialized => nuberOfLTVsAfter ==  assert_uint256(nuberOfLTVsBefore +1), "Uninitalized LTV is not added to the ltvList");
    // }

     //setInterestRateModel works 
    rule setInterestRateModelIntegraty(env e) {
        address newInterestRateModel;
        GovernanceHarness.VaultCache targetVaultCache = getVaultCacheHarness(e);
        uint256 ghostInterestRate = GhostCalculatedInterestRate[currentContract];
        uint72 calculatedInterestRate = assert_uint72(calculateInterestRateHarness(e, ghostInterestRate));

        //function call
        setInterestRateModel(e, newInterestRateModel);

        //values after
        address interestRateModelAfter = interestRateModel();
        uint72 interestRateAfter = getInterestRateHarness();

        //ASSERTS
        //assert1:interest rate model is set correctly
        assert(interestRateModelAfter == newInterestRateModel, "Interest rate model was not set correctly");

        //asert2:if newInterestRateModel is address(0), the interes rate should be 0
        assert(newInterestRateModel == 0 => interestRateAfter == 0, "Interest rate should be 0");

        //assert3:if irm != 0 interest rate is updated
        assert(interestRateModelAfter != 0 => interestRateAfter == calculatedInterestRate, "Interest rate was not updated correctly");

    }

    //only spesific functions should change HookConfig
    rule onlyChangeHookConfig(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        address hookTargetBefore;
        uint32 hookedOpsBefore;
        (hookTargetBefore, hookedOpsBefore) = hookConfig();

        f(e, args);

        address hookTargetAfter;
        uint32 hookedOpsAfter;
        (hookTargetAfter, hookedOpsAfter) = hookConfig();

        assert(hookTargetBefore != hookTargetAfter || hookedOpsBefore != hookedOpsAfter => 
        f.selector == sig:setHookConfig(address,uint32).selector, "HookConfig was changed by unothorised function");
    }

    //only spesific functions should change supplyCaps 
    rule onlyChangeSupplyCaps(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        uint16 supplyCapBefore;
        uint16 borrowCapBefore;
        (supplyCapBefore, borrowCapBefore) = caps();

        f(e, args);

        uint16 supplyCapAfter;
        uint16 borrowCapAfter;
        (supplyCapAfter, borrowCapAfter) = caps();

        assert(supplyCapBefore != supplyCapAfter  || borrowCapBefore != borrowCapAfter => f.selector == sig:setCaps(uint16,uint16).selector, "Supply caps were changed by unothorised function");
    }

    //only spesific functions should change accumulatedFees 
    rule onlyChangeAccumulatedFees(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        GovernanceHarness.Shares accumulatedFeesBefore = getCurrentVaultCacheHarness().accumulatedFees;

        f(e, args);

        GovernanceHarness.Shares accumulatedFeesAfter = getCurrentVaultCacheHarness().accumulatedFees;

        assert(accumulatedFeesBefore != accumulatedFeesAfter =>
        f.selector == sig:convertFees().selector, "Accumulated fees was changed by unothorised function");
    }

    //only spesific functions should change InterestFee
    rule onlyChangeInterestFee(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        uint16 interestFeeBefore = interestFee();

        f(e, args);

        uint16 interestFeeAfter = interestFee();

        assert(interestFeeBefore != interestFeeAfter => 
        f.selector == sig:setInterestFee(uint16).selector, "InterestFee was changed by unothorised function");
    }


    //only spesific functions should change ConfigFlags
    rule onlyChangeConfigFlags(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        uint32 configFlagsBefore = configFlags();

        f(e, args);

        uint32 configFlagsAfter = configFlags();

        assert(configFlagsBefore != configFlagsAfter => 
        f.selector == sig:setConfigFlags(uint32).selector, "ConfigFlags were changed by unothorised function");
    }
    
    //only spesific functions should change FeeReceiver
    rule onlyChangeFeeReceiver(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        address feeReceiverBefore = feeReceiver();

        f(e, args);

        address feeReceiverAfter = feeReceiver();

        assert(feeReceiverBefore != feeReceiverAfter => 
        f.selector == sig:setFeeReceiver(address).selector, "FeeReceiver was changed by unothorised function");
    }

    //only spesific functions should change GovernorAdmin
    rule onlyChangeGovernorAdmin(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        address governorAdminBefore = governorAdmin();

        f(e, args);

        address governorAdminAfter = governorAdmin();

        assert(governorAdminBefore != governorAdminAfter => 
        f.selector == sig:setGovernorAdmin(address).selector, "GovernorAdmin was changed by unothorised function");
    }

    //only spesific functions should change InterestRateModel
    rule onlyChangeInterestRateModel(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        address interestRateModelBefore = interestRateModel();
        uint72 interestRateBefore = interestRateHarness();

        f(e, args);

        address interestRateModelAfter = interestRateModel();
        uint72 interestRateAfter = interestRateHarness();

        assert(interestRateModelBefore != interestRateModelAfter || interestRateBefore != interestRateAfter => 
        f.selector == sig:setInterestRateModel(address).selector, "InterestRateModel was changed by unothorised function");
    }

    //only spesific functions should change LiquidationCoolOffTime
    rule onlyChangeLiquidationCoolOffTime(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        uint16 liquidationCoolOffTimeBefore = liquidationCoolOffTime();

        f(e, args);

        uint16 liquidationCoolOffTimeAfter = liquidationCoolOffTime();

        assert(liquidationCoolOffTimeBefore != liquidationCoolOffTimeAfter => 
        f.selector == sig:setLiquidationCoolOffTime(uint16).selector, "LiquidationCoolOffTime was changed by unothorised function");
    }

    //only spesific functions should change LTV
    rule onlyChangeLTV(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        address collateral;
        uint16 borrowLTVBefore;
        uint16 liquidationLTVBefore;
        uint16 initialLiquidationLTVBefore;
        uint48 targetTimestampBefore;
        uint32 rampDurationBefore;
        (borrowLTVBefore, liquidationLTVBefore, initialLiquidationLTVBefore, targetTimestampBefore, rampDurationBefore) = LTVFull(collateral);
        bool isInitializedBefore = getCurrentLTVConfigHarness(collateral).initialized;
        uint256 numberOfLTVsBefore = LTVList().length;


        f(e, args);

        uint16 borrowLTVAfter;
        uint16 liquidationLTVAfter;
        uint16 initialLiquidationLTVAfter;
        uint48 targetTimestampAfter;
        uint32 rampDurationAfter;
        (borrowLTVAfter, liquidationLTVAfter, initialLiquidationLTVAfter, targetTimestampAfter, rampDurationAfter) = LTVFull(collateral);
        bool isInitializedAfter = getCurrentLTVConfigHarness(collateral).initialized;
        uint256 numberOfLTVsAfter = LTVList().length;

        assert(borrowLTVBefore != borrowLTVAfter || liquidationLTVBefore != liquidationLTVAfter || initialLiquidationLTVBefore != initialLiquidationLTVAfter || targetTimestampBefore != targetTimestampAfter || rampDurationBefore != rampDurationAfter || isInitializedBefore != isInitializedAfter || numberOfLTVsAfter != numberOfLTVsBefore => 
        f.selector == sig:setLTV(address,uint16,uint16,uint32).selector ||
        f.selector == sig:clearLTV(address).selector
        , "LTV was changed by unothorised function");
    }

    //only spesific functions should change MaxLiquidationDiscount
    rule onlyChangeMaxLiquidationDiscount(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f)}{
        uint16 maxLiquidationDiscountBefore = maxLiquidationDiscount();

        f(e, args);

        uint16 maxLiquidationDiscountAfter = maxLiquidationDiscount();

        assert(maxLiquidationDiscountBefore != maxLiquidationDiscountAfter => 
        f.selector == sig:setMaxLiquidationDiscount(uint16).selector, "MaxLiquidationDiscount was changed by unothorised function");
    }

    // convertFees works
    rule convertFeesIntegraty(env e) {
    //VALUES BEFORE
        //addresses
        address protocolReceiver;
        uint16 protocolFee;
        (protocolReceiver, protocolFee) = ProtocolConfig.protocolFeeConfig(e,currentContract);
        GovernanceHarness.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address governerReceiver = getGovernorReceiverHarness();
        require(protocolReceiver != governerReceiver);
        address user;
        require(user != governerReceiver && user != protocolReceiver);
        GovernanceHarness.Shares sharesBefore = getTotalSharesHarness();
        uint16 finalProtocolFee = calculateProtocolFeeHarness(governerReceiver, protocolFee);

        //Shares to move
        GovernanceHarness.Shares governorSharesToAdd;
        GovernanceHarness.Shares protocolSharesToAdd;
        (governorSharesToAdd, protocolSharesToAdd) = calculateSharesToMoveHarness(e, vaultCacheBefore.accumulatedFees, finalProtocolFee);

        //Balances
        GovernanceHarness.PackedUserSlot userDataBefore = getUserStorageDataHarness(user);
        GovernanceHarness.PackedUserSlot governerReceiverDataBefore = getUserStorageDataHarness(governerReceiver);
        GovernanceHarness.PackedUserSlot protocolReceiverDataBefore = getUserStorageDataHarness(protocolReceiver);
        GovernanceHarness.Shares governorReceiverSharesBefore = unpackBalanceHarness(governerReceiverDataBefore);
        GovernanceHarness.Shares protocolReceiverSharesBefore = unpackBalanceHarness(protocolReceiverDataBefore);

    //FUNCTION CALL
        convertFees(e);

    //VALUES AFTER
        //Balances
        GovernanceHarness.PackedUserSlot userDataAfter = getUserStorageDataHarness(user);
        GovernanceHarness.Shares sharesAfter = getTotalSharesHarness();
        GovernanceHarness.PackedUserSlot governerReceiverDataAfter = getUserStorageDataHarness(governerReceiver);
        GovernanceHarness.PackedUserSlot protocolReceiverDataAfter = getUserStorageDataHarness(protocolReceiver);
        GovernanceHarness.Shares governorReceiverSharesAfter = unpackBalanceHarness(governerReceiverDataAfter);
        GovernanceHarness.Shares protocolReceiverSharesAfter = unpackBalanceHarness(protocolReceiverDataAfter);
        GovernanceHarness.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();

    //ASSERTS
        // assert1: balance of no othere account changes 
        assert(userDataBefore == userDataAfter, "Balances has changed");

            // assert2: total shares should be the same as before
        assert(sharesBefore == sharesAfter, "Total shares have changed");

        // assert3: balance of governerReceiver should be added propperly
        assert(to_mathint(governorReceiverSharesAfter) == governorReceiverSharesBefore + governorSharesToAdd, "Governer receiver balance has not changed propperly");

        // assert4: balance of protocolReceiver should be added propperly
        assert(to_mathint(protocolReceiverSharesAfter) == protocolReceiverSharesBefore + protocolSharesToAdd, "Protocol receiver balance has not changed propperly");

        // assert5: accumulated fees should be 0
        assert(vaultCacheAfter.accumulatedFees == 0, "Accumulated fees is not 0");    
    } 

    //setLTV reverts check
    rule setLTVRevertIntegraty(env e) {
        address collateral;
        uint16 borrowLTV;
        uint16 liquidationLTV;
        uint32 rampDuration;

        //VALUES BEFORE
        GovernanceHarness.LTVConfig ltvConfigBefore = getCurrentLTVConfigHarness(collateral);
        GovernanceHarness.ConfigAmount currentTvlBefore = calculateLiquidationLTVHarness(e, ltvConfigBefore, true);

        

        //FUNCTION CALL
        setLTV@withrevert(e, collateral, borrowLTV, liquidationLTV, rampDuration);
        bool reverted = lastReverted;


        //ASSERTS
        //assert1:revert if collataral = currentContract
        assert(collateral == currentContract => reverted, "Collateral is the current contract");

        //assert2:revert if borrowLTV > liquidationLTV
        assert(borrowLTV > liquidationLTV => reverted, "Borrow LTV is bigger than liquidation LTV");

        //assert3:revert if new liquidationLTV >= currentTvlBefore and rampDuration > 0, revert
        assert(liquidationLTV >= currentTvlBefore && rampDuration > 0 => reverted, "Function should revert");
    }

    //setInterestFee works 
    rule setInterestFeeIntegraty(env e) {
        uint16 newInterestFee;
        bool checkValidity = newInterestFee < getGUARANTEED_INTEREST_FEE_MINHarness() || newInterestFee > getGUARANTEED_INTEREST_FEE_MAXHarness();
        bool validInteresFee = isValidInterestFeeHarness(newInterestFee);

        //@audit issues would be in contracts without mutations:
        //get all values from the cache before and after
        //if time hast not passed, then values after need to be the same as before

        //function call
        setInterestFee@withrevert(e, newInterestFee);
        bool reverted = lastReverted;

        //interestFee value after
        uint16 interestFeeAfter = interestFee();

        assert(!reverted => interestFeeAfter == newInterestFee, "Interest fee was not set correctly");
        assert(!validInteresFee && checkValidity => reverted, "Interest fee is not valid");
    }

    //setHookConfig works 
    rule setHookConfigIntegraty(env e) {
        address newHookTarget;
        uint32 hookedOps;
        GovernanceHarness.Flags wrapedHookedOps = wrapFlagsHarness(hookedOps);
        require(HookTarget == newHookTarget);
        bytes4 targetSelector = isHookTarget();
        bytes4 selector = HookTarget.isHookTarget(e);
        address onBehalfOf = getOnBehalfOfAccountHarness(e);
        bool lockedBefore = reentrancyLockedHarness();


        //function call
        setHookConfig@withrevert(e, newHookTarget, hookedOps);
        bool reverted = lastReverted;

        //hookConfig values after
        address hookTargetAfter;
        uint32 hookedOpsAfter;
        (hookTargetAfter, hookedOpsAfter) = hookConfig();

        //if newHookTarget != address(0) and the selector is not the correct one, revert
        assert(newHookTarget != 0 && selector != targetSelector => reverted, "The selector is not the right one");

        //if the hookedOps is bigger or equal to OP_MAX_VALUE, revert
        assert(hookedOps >= getOP_MAX_VALUEHarness() => reverted, "Hooked ops value is too high");

        //when function passes, the data is set correctly
        assert(!reverted => hookTargetAfter == newHookTarget && hookedOpsAfter == wrapedHookedOps, "Hook config values were not set correctly");
    }

    // Spesific state variables can only be changed by the governor
    rule onlyGovernorCanChangeStateVariables(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !HARNESS_FUNCTIONS(f) && !DISABLED_FUNCTIONS(f) && f.selector != sig:convertFees().selector}{
        address onBehalfeOf = getOnBehalfOfAccountHarness(e); 
        address governorAdmin = governorAdmin();

        //BEFORE: variables that can only be changed by the governor
        address governorAdminBefore = governorAdmin();
        address feeReceiverBefore = feeReceiver();
        uint16 maxLiquidationDiscountBefore = maxLiquidationDiscount();
        uint16 liquidationCoolOffTimeBefore = liquidationCoolOffTime();
        address interestRateModelBefore = interestRateModel();
        uint32 configFlagsBefore = configFlags();
        uint16 cap1Before;
        uint16 cap2Before;
        (cap1Before, cap2Before) = caps();
        uint16 interestFeeBefore = interestFee();
        address hookTargetBefore;
        uint32 hookedOpsBefore;
        (hookTargetBefore, hookedOpsBefore) = hookConfig(); 
        //LTV values
        address collateral;
        uint16 borrowLTVBefore;
        uint16 liquidationLTVBefore;
        uint16 initialLiquidationLTVBefore; //not used
        uint48 targetTimestampBefore; //not used
        uint32 rampDurationBefore;
        (borrowLTVBefore, liquidationLTVBefore, initialLiquidationLTVBefore, targetTimestampBefore, rampDurationBefore) = LTVFull(collateral);

        //function call
        f(e, args);

        //AFTRE: variables that can only be changed by the governor
        address governorAdminAfter = governorAdmin();
        address feeReceiverAfter = feeReceiver();
        uint16 maxLiquidationDiscountAfter = maxLiquidationDiscount();
        uint16 liquidationCoolOffTimeAfter = liquidationCoolOffTime();
        address interestRateModelAfter = interestRateModel();
        uint32 configFlagsAfter = configFlags();
        uint16 cap1After;
        uint16 cap2After;
        (cap1After, cap2After) = caps();
        uint16 interestFeeAfter = interestFee();
        address hookTargetAfter;
        uint32 hookedOpsAfter;
        (hookTargetAfter, hookedOpsAfter) = hookConfig(); 
        //LTV values
        uint16 borrowLTVAfter;
        uint16 liquidationLTVAfter;
        uint16 initialLiquidationLTVAfter; //not used
        uint48 targetTimestampAfter; //not used
        uint32 rampDurationAfter;
        (borrowLTVAfter, liquidationLTVAfter, initialLiquidationLTVAfter, targetTimestampAfter, rampDurationAfter) = LTVFull(collateral);

        assert(
            governorAdminBefore != governorAdminAfter ||
            feeReceiverBefore != feeReceiverAfter ||
            maxLiquidationDiscountBefore != maxLiquidationDiscountAfter ||
            liquidationCoolOffTimeBefore != liquidationCoolOffTimeAfter ||
            interestRateModelBefore != interestRateModelAfter ||
            configFlagsBefore != configFlagsAfter ||
            cap1Before != cap1After ||
            cap2Before != cap2After ||
            interestFeeBefore != interestFeeAfter ||
            hookTargetBefore != hookTargetAfter ||
            hookedOpsBefore != hookedOpsAfter ||
            borrowLTVBefore != borrowLTVAfter ||
            liquidationLTVBefore != liquidationLTVAfter ||
            rampDurationBefore != rampDurationAfter     
            => onBehalfeOf == governorAdmin, "State variables were changed by someone else than the governor admin");

    }

    //setCaps works
    rule setCapsIntegraty(env e) {
        uint16 supplyCap;
        uint16 borrowCap;
        GovernanceHarness.AmountCap _supplyCap = wrapAmountCapHarness(supplyCap);
        uint256 resolvedSupplyCap = resolveAmountCapHarness(_supplyCap);
        GovernanceHarness.AmountCap _borrowCap = wrapAmountCapHarness(borrowCap);
        uint256 resolvedBorrowCap = resolveAmountCapHarness(_borrowCap);

        
        //function call
        setCaps@withrevert(e, supplyCap, borrowCap);
        bool reverted = lastReverted;
        
        //caps values after
        uint16 supplyCapAfter;
        uint16 borrowCapAfter;
        (supplyCapAfter, borrowCapAfter) = caps();

        //if the function does not revert, the caps are set correctly
        assert(!reverted => supplyCapAfter == _supplyCap && borrowCapAfter == _borrowCap, "Caps values were not set correctly");

        // if supplyCap != 0 and resolvedSupplyCap is to big, the function should revert
        assert(supplyCap != 0 && resolvedSupplyCap > assert_uint256(2 * getMAX_SANE_AMOUNTHarness()) => reverted, "Supply cap is too high");

        //if borrowCap != 0 and resolvedBorrowCap is to big, the function should revert
        assert(borrowCap != 0 && resolvedBorrowCap > getMAX_SANE_AMOUNTHarness() => reverted, "Borrow cap is too high"); 
    }

    //setLiquidationCoolOffTime works
    rule setLiquidationCoolOffTimeIntegraty(env e) {
        uint16 liquidationCoolOffTime;

        //function call
        setLiquidationCoolOffTime(e, liquidationCoolOffTime);

        //liquidationCoolOffTime value after
        uint16 liquidationCoolOffTimeAfter = liquidationCoolOffTime();

        assert(liquidationCoolOffTimeAfter == liquidationCoolOffTime, "Liquidation cool off time was not set correctly");
    }

    //setMaxLiquidationDiscount works
    rule setMaxLiquidationDiscountIntegraty(env e) {
        uint16 maxLiquidationDiscount;

        //function call
        setMaxLiquidationDiscount(e, maxLiquidationDiscount);

        //maxLiquidationDiscount value after
        uint16 maxLiquidationDiscountAfter = maxLiquidationDiscount();

        assert(maxLiquidationDiscountAfter == maxLiquidationDiscount, "Max liquidation discount was not set correctly");
    }

    //setConfigFlags works
    rule setConfigFlagsIntegraty(env e) {
        uint32 configFlags;

        //function call
        setConfigFlags@withrevert(e, configFlags);
        bool reverted = lastReverted;

        //configFlags values after
        uint32 configFlagsAfter = configFlags();

        assert(!reverted => configFlagsAfter == configFlags, "Config flags were not set correctly");
        assert(configFlags >= getCFG_MAX_VALUEHarness() => reverted, "Config flags value is too high");
    }

    //setGovernorAdmin works
    rule setGovernorAdminIntegraty(env e) {
        address governorAdmin;
        
        //function call
        setGovernorAdmin(e, governorAdmin);

        //governorAdmin value after
        address governorAdminAfter = governorAdmin();

        assert(governorAdminAfter == governorAdmin, "Governor admin was not set correctly");
    }

    //setFeeReceiver works
    rule setFeeReceiverIntegraty(env e) {
        address feeReceiver;
        
        //function call
        setFeeReceiver(e, feeReceiver);

        //feeReceiver value after
        address feeReceiverAfter = feeReceiver();

        assert(feeReceiverAfter == feeReceiver, "Fee receiver was not set correctly");
    }

    //clearLTV works
    rule clearLTVIntegraty(env e) {
        address collateral;
        
        //function call
        clearLTV(e, collateral);
        
        //LTV values after
        uint16 borrowLTVAfter;
        uint16 liquidationLTVAfter;
        uint16 initialLiquidationLTVAfter;
        uint48 targetTimestampAfter;
        uint32 rampDurationAfter;
        (borrowLTVAfter, liquidationLTVAfter, initialLiquidationLTVAfter, targetTimestampAfter, rampDurationAfter) = LTVFull(collateral);

        assert(borrowLTVAfter == 0 && liquidationLTVAfter == 0 && initialLiquidationLTVAfter == 0 && targetTimestampAfter == 0 && rampDurationAfter == 0, "LTV values were not cleared");
    }

    //Functions can only be called by the governor and revert if someone else calls them
    rule onlyGovernorCanCall(env e, method f, calldataarg args) filtered{f -> GOVERNOR_ADMIN_ONLY_FUNCTIONS(f)}{

        address onBehalfeOf = getOnBehalfOfAccountHarness(e); 
        address governorAdmin = governorAdmin();

        f(e, args);

        assert(!lastReverted => onBehalfeOf == governorAdmin, "Caller is not the governor admin");

    }

    //functions need to revert if reentrancy is locked
    rule reentrancyLockIntegraty(env e, method f, calldataarg args) filtered{f -> GOVERNOR_ADMIN_ONLY_FUNCTIONS(f) || f.selector == sig:convertFees().selector}{
 
        bool lockedBefore = reentrancyLockedHarness();
        f@withrevert(e, args);

        assert(lockedBefore => lastReverted, "Reentrancy lock did not work");
    }

//------------------------------- RULES OK END ------------------------------------

//-------------------------------RULES GET OK START ----------------------------------

    // // getting LTVList works //@audit-check worked and now does not work
    // rule getLTVListIntegraty(env e) {
    //     address[] LTVList = LTVListHarness(e);

    //     //function call
    //     address[] LTVListCall = LTVList();
    //     uint256 i = LTVListCall.length;

    //     assert(LTVListCall[i] == LTVList[i], "LTV list was not returned correctly");
    // }

    // getting maxLiquidationDiscount works
    rule getMaxLiquidationDiscountIntegraty(env e) {
        uint16 maxLiquidationDiscount = Governance.vaultStorage.maxLiquidationDiscount;

        //function call
        uint16 maxLiquidationDiscountCall = maxLiquidationDiscount();

        assert(maxLiquidationDiscountCall == maxLiquidationDiscount, "Max liquidation discount was not returned correctly");
    }

    // getting oracle works 
    rule getOracleIntegraty(env e) {
        address oracle = oracleHarness(e);

        //function call
        address oracleCall = oracle();

        assert(oracleCall == oracle, "Oracle was not returned correctly");
    }

    // getting permit2Address works
    rule getPermit2AddressIntegraty(env e) {
        address permit2Address = Governance.permit2;

        //function call
        address permit2AddressCall = permit2Address();

        assert(permit2AddressCall == permit2Address, "Permit2 address was not returned correctly");
    }

    // getting protocolConfigAddress works
    rule getProtocolConfigAddressIntegraty(env e) {
        address protocolConfigAddress = Governance.protocolConfig;

        //function call
        address protocolConfigAddressCall = protocolConfigAddress();

        assert(protocolConfigAddressCall == protocolConfigAddress, "Protocol config address was not returned correctly");
    }

     //getting governorAdmin works
    rule getGovernorAdminIntegraty(env e) {
        address governorAdmin = Governance.vaultStorage.governorAdmin;

        //function call
        address governorAdminCall = governorAdmin();

        assert(governorAdminCall == governorAdmin, "Governor admin was not returned correctly"); 
    }

    //getting feeReceiver works
    rule getFeeReceiverIntegraty(env e) {
        address feeReceiver = Governance.vaultStorage.feeReceiver;

        //function call
        address feeReceiverCall = feeReceiver();

        assert(feeReceiverCall == feeReceiver, "Fee receiver was not returned correctly");
    }

    //getting interestFee works
    rule getInterestFeeIntegraty(env e) {
        uint16 interestFee = Governance.vaultStorage.interestFee;

        //function call
        uint16 interestFeeCall = interestFee();

        assert(interestFeeCall == interestFee, "Interest fee was not returned correctly");
    }

    //getting interestRateModel works
    rule getInterestRateModelIntegraty(env e) {
        address interestRateModel = Governance.vaultStorage.interestRateModel;

        //function call
        address interestRateModelCall = interestRateModel();

        assert(interestRateModelCall == interestRateModel, "Interest rate model was not returned correctly");
    }

    // getting caps works
    rule getCapsIntegraty(env e) {
        uint16 supplyCap = Governance.vaultStorage.supplyCap;
        uint16 borrowCap = Governance.vaultStorage.borrowCap;

        //function call
        uint16 supplyCapCall;
        uint16 borrowCapCall;
        (supplyCapCall, borrowCapCall) = caps();

        assert(supplyCapCall == supplyCap && borrowCapCall == borrowCap, "Caps were not returned correctly");
    }

    // getting configFlags works
    rule getConfigFlagsIntegraty(env e) {
        uint32 configFlags = Governance.vaultStorage.configFlags;
        
        //function call
        uint32 configFlagsCall = configFlags();

        assert(configFlagsCall == configFlags, "Config flags were not returned correctly");
    }

    // getting EVC works 
    rule getEVCIntegraty(env e) {
        address EVC = EVCHarness(e);

        //function call
        address EVCCall = EVC();

        assert(EVCCall == EVC, "EVC was not returned correctly");
    }

    // getting hookConfig works
    rule getHookConfigIntegraty(env e) {
        address hookTarget = Governance.vaultStorage.hookTarget;
        uint32 hookedOps = Governance.vaultStorage.hookedOps;

        //function call
        address hookTargetCall;
        uint32 hookedOpsCall;
        (hookTargetCall, hookedOpsCall) = hookConfig();

        assert(hookTargetCall == hookTarget && hookedOpsCall == hookedOps, "Hook config was not returned correctly");
    }

    // getting liquidationCoolOffTime works
    rule getLiquidationCoolOffTimeIntegraty(env e) {
        uint16 liquidationCoolOffTime = Governance.vaultStorage.liquidationCoolOffTime;

        //function call
        uint16 liquidationCoolOffTimeCall = liquidationCoolOffTime();

        assert(liquidationCoolOffTimeCall == liquidationCoolOffTime, "Liquidation cool off time was not returned correctly");
    }

    // getting LTVBorrow(address) works
    rule getLTVBorrowIntegraty(env e) {
        address collateral;
        uint16 borrowLTV = Governance.vaultStorage.ltvLookup[collateral].borrowLTV; 

        //function call
        uint16 borrowLTVCall = LTVBorrow(e,collateral);

        assert(borrowLTVCall == borrowLTV, "Borrow LTV was not returned correctly");
    }

    // getting LTVFull(address) works
    rule getLTVFullIntegraty(env e) {
        address collateral;
        uint16 borrowLTV = Governance.vaultStorage.ltvLookup[collateral].borrowLTV;
        uint16 liquidationLTV = Governance.vaultStorage.ltvLookup[collateral].liquidationLTV;
        uint16 initialLiquidationLTV = Governance.vaultStorage.ltvLookup[collateral].initialLiquidationLTV;
        uint48 targetTimestamp = Governance.vaultStorage.ltvLookup[collateral].targetTimestamp;
        uint32 rampDuration = Governance.vaultStorage.ltvLookup[collateral].rampDuration;

        //function call
        uint16 borrowLTVCall;
        uint16 liquidationLTVCall;
        uint16 initialLiquidationLTVCall;
        uint48 targetTimestampCall;
        uint32 rampDurationCall;
        (borrowLTVCall, liquidationLTVCall, initialLiquidationLTVCall, targetTimestampCall, rampDurationCall) = LTVFull(collateral);

        assert(borrowLTVCall == borrowLTV && liquidationLTVCall == liquidationLTV && initialLiquidationLTVCall == initialLiquidationLTV && targetTimestampCall == targetTimestamp && rampDurationCall == rampDuration, "LTV values were not returned correctly");
    }



//-------------------------------RULES GET OK END ----------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

