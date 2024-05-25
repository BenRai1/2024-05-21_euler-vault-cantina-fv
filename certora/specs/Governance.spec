import "./Base.spec";
import "./Base/governance.spec";
using MockHookTarget as HookTarget;
using ProtocolConfig as ProtocolConfig;

// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants:
//- interstRate should never be bigger than MAX_ALLOWED_INTEREST_RATE
//- lastInterestAccumulatorUpdate should never be bigger than the current block timestamp
//- totalBorrowed should never be bigger than totalShares
//- borrowLTV should never be bigger than liquidationLTV

//------------------------------- RULES TEST START ----------------------------------

//convertFees reverts
rule convertFeesRevertIntegraty(env e) {
    //GENERAL VARIABLES
    address actualCaller = actualCaller(e);
    address user;
        
    //VALUES BEFORE
    GovernanceHarness.VaultCache vaultCacheBefore = getVaultCacheHarness(e);
    address protocolReceiver;
    uint16 protocolFee;
    (protocolReceiver, protocolFee) = ProtocolConfig.protocolFeeConfig(e,currentContract);
    //Balances
    GovernanceHarness.PackedUserSlot userDataBefore = getUserStorageDataHarness(user);

    //FUNCTION CALL
    convertFees@withrevert(e);
    bool reverted = lastReverted;

    //VALUES AFTER
    GovernanceHarness.VaultCache vaultCacheAfter = getVaultCacheHarness(e);
    GovernanceHarness.PackedUserSlot userDataAfter = getUserStorageDataHarness(user);



    //ASSERTS
    // //assert2: if vaultCache.accumulatedFees = 0, stuff should not change
    // assert(vaultCacheBefore.accumulatedFees == 0 => 
    // vaultCacheBefore.accumulatedFees == vaultCacheAfter.accumulatedFees &&
    // userDataBefore == userDataAfter,
    //  "Accumulated fees or balances changed");

    //assert3: if the protocolReceiver = 0 address, revert
    assert(vaultCacheBefore.accumulatedFees != 0 && protocolReceiver == 0 && protocolFee != 0 => reverted, "Protocol receiver is 0");


    ///------------------------------- ASSERTS OK START ------------------------------
        // //assert1: if hook target is zero address, revert
        // assert(actualCaller == 0 => reverted, "ActualCaller is 0");
}


// convertFees works
rule convertFeesIntegraty(env e) {
  //VALUES BEFORE
    //addresses
    address protocolReceiver;
    uint16 protocolFee;
    (protocolReceiver, protocolFee) = ProtocolConfig.protocolFeeConfig(e,currentContract);
    address governerReceiver = getGovernorReceiverHarness();
    address user;
    require(user != governerReceiver && user != protocolReceiver);
    GovernanceHarness.Shares sharesBefore = getTotalSharesHarness();
    uint16 finalProtocolFee = calculateProtocolFeeHarness(governerReceiver, protocolFee);

    //Shares to move
    GovernanceHarness.Shares governorSharesToAdd;
    GovernanceHarness.Shares protocolSharesToAdd;
    (governorSharesToAdd, protocolSharesToAdd) = calculateSharesToMoveHarness(e, sharesBefore, finalProtocolFee);

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



  //ASSERTS
      // assert1: balance of no othere account changes //@audit test of summary
    assert(userDataBefore == governerReceiverDataBefore, "Balances has changed");

    // // assert2: total shares should be the same as before
    // assert(sharesBefore == sharesAfter, "Total shares have changed");

    // // assert3: balance of governerReceiver should be added propperly
    // assert(to_mathint(governorReceiverSharesAfter) == governorReceiverSharesBefore + governorSharesToAdd, "Governer receiver balance has not changed");

    // // assert4: balance of protocolReceiver should be added propperly
    // assert(to_mathint(protocolReceiverSharesAfter) == protocolReceiverSharesBefore + protocolSharesToAdd, "Protocol receiver balance has not changed");

    // assert5: accumulated fees should be 0

   ///------------------------------- ASSERTS OK START ------------------------------
    // // assert1: balance of no othere account changes 
    // assert(userDataBefore == userDataAfter, "Balances has changed");
    



} 



   



//------------------------------- TESTING ----------------------------------


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

    //setInterestRateModel works //@audit targetInterestRate rate is not calculated propperly and fails
    rule setInterestRateModelIntegraty(env e) {
        address newInterestRateModel;
        GovernanceHarness.VaultCache targetVaultCache = getVaultCacheHarness(e); ////@audit assume this works (??)
        //check if targetVaultCache workes
        // if so, use it to get the targetInterestRate
        uint256 targetInterestRate = getTargetInterestRateHarness(e,newInterestRateModel, targetVaultCache);

        //function call
        setInterestRateModel(e, newInterestRateModel);

        //values after
        address interestRateModelAfter = interestRateModel();
        uint72 interestRateAfter = getInterestRateHarness();

        //--------------------------------- ASSERTS OK START ------------------------------
            // //interest rate model is set correctly
            // assert(interestRateModelAfter == newInterestRateModel, "Interest rate model was not set correctly");

            // //if newInterestRateModel is address(0), the interes rate should stay the same
            // assert(newInterestRateModel == 0 => interestRateAfter == 0, "Interest rate should be 0");

        ///------------------------------- ASSERTS OK END ------------------------------

        //interest rate is updated
        assert(interestRateAfter == assert_uint72(targetInterestRate), "Interest rate was not updated correctly");

        //check if the 



        //@audit issues would be in contracts without mutations:
        //get all values from the cache before and after
        //if time hast not passed, then values after need to be the same as before
    }


 //setLTV works //@audit checking the final values does not work becasue the State is still HAVOC https://prover.certora.com/output/8418/8704acbf970745d48b8a36270f527f22/?anonymousKey=978dcc2b6dce63ce294f88c72039f62b81533215
    rule setLTVIntegraty(env e) {
        address collateral;
        require(collateral != 0);
        uint16 borrowLTV;
        GovernanceHarness.ConfigAmount newBorrowLTV = toConfigAmountHarness(borrowLTV);
        uint16 liquidationLTV;
        GovernanceHarness.ConfigAmount newLiquidationLTV = toConfigAmountHarness(liquidationLTV);
        uint32 rampDuration;

        //VALUES BEFORE
        GovernanceHarness.LTVConfig ltvConfigBefore = getCurrentLTVConfigHarness(collateral); 
        bool isInitialized = ltvConfigBefore.initialized;
        GovernanceHarness.ConfigAmount currentTvlBefore = calculateLiquidationLTVHarness(e, ltvConfigBefore, true);
        uint256 nuberOfLTVsBefore = LTVList().length;



        //FUNCTION CALL
        setLTV(e, collateral, borrowLTV, liquidationLTV, rampDuration);
        

        //VALUES AFTER
        GovernanceHarness.LTVConfig LTVConfigAfter = getCurrentLTVConfigHarness(collateral);
        uint256 nuberOfLTVsAfter = LTVList().length;

        //maybe try this
        //LTV values after
        // uint16 borrowLTVAfter;
        // uint16 liquidationLTVAfter;
        // uint16 initialLiquidationLTVAfter;
        // uint48 targetTimestampAfter;
        // uint32 rampDurationAfter;
        // (borrowLTVAfter, liquidationLTVAfter, initialLiquidationLTVAfter, targetTimestampAfter, rampDurationAfter) = LTVFull(collateral);



        //ASSERTS
        // //assert1: borrowLTVAfter = newBorrowLTV 
        // assert(LTVConfigAfter.borrowLTV == newBorrowLTV, "Borrow LTV was not set correctly");

        // //assert2: liquidationLTVAfter = liquidationLTV
        // assert(LTVConfigAfter.liquidationLTV == newLiquidationLTV, "Liquidation LTV was not set correctly");

        // //assert3: initialLiquidationLTVAfter = ???
        // assert(LTVConfigAfter.initialLiquidationLTV == currentTvlBefore, "Initial liquidation LTV was not set correctly");

        // //assert4: targetTimestampAfter = e.block.timestamp + rampDuration
        // assert(LTVConfigAfter.targetTimestamp == assert_uint48(e.block.timestamp + rampDuration), "Target timestamp was not set correctly");

        // //assert5: rampDurationAfter = rampDuration
        // assert(LTVConfigAfter.rampDuration == rampDuration, "Ramp duration was not set correctly");

        // //assert6: currentLtvConfigAfter.initialized = true
        // assert(LTVConfigAfter.initialized == true, "Initialized was not set correctly");

        //--------------------------------- ASSERTS OK START ------------------------------
        
            // //assert7: if !initailized, the LTV is added to the LTVList
            assert(!isInitialized => nuberOfLTVsAfter ==  assert_uint256(nuberOfLTVsBefore +1), "Uninitalized LTV is not added to the ltvList");

        //--------------------------------- ASSERTS OK END ------------------------------
    }
   



//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------





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

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

