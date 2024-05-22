import "./Base.spec";
import "./Base/governance.spec";
using MockHookTarget as HookTarget;

// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants:
//- interstRate should never be bigger than MAX_ALLOWED_INTEREST_RATE
//- lastInterestAccumulatorUpdate should never be bigger than the current block timestamp

//------------------------------- RULES TEST START ----------------------------------



    //setInterestRateModel works //@audit Vault must be updated first, must be in the range
    rule setInterestRateModelIntegraty(env e) {
        address newInterestRateModel;
        GovernanceHarness.VaultCache targetVaultCache = getVaultCacheHarness(e); ////@audit assume this works
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





   



//------------------------------- TESTING ----------------------------------


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------




        //setLTV works //@audit reverts work, checking the final values does not work
    rule setLTVIntegraty(env e) {
        address collateral;
        uint16 borrowLTV;
        GovernanceHarness.ConfigAmount newBorrowLTV = toConfigAmountHarness(borrowLTV);
        uint16 liquidationLTV;
        GovernanceHarness.ConfigAmount newLiquidationLTV = toConfigAmountHarness(liquidationLTV);
        uint32 rampDuration;
        GovernanceHarness.LTVConfig currentLtvConfigBefore = getCurrentLTVConfigHarness(collateral); 
        GovernanceHarness.ConfigAmount calculatedTvl = getLTVHarness(e, currentLtvConfigBefore, true);
        bool isInitialized = currentLtvConfigBefore.initialized;
        uint256 nuberOfLTVsBefore = LTVList().length;
        require(nuberOfLTVsBefore < max_uint256);
        require(e.block.timestamp + rampDuration < max_uint48);
        bool lockedBefore = reentrancyLockedHarness();
        address onBehalfeOf = getOnBehalfOfAccountHarness(e);



        //LTV values before
        uint16 borrowLTVBefore;
        uint16 liquidationLTVBefore;
        uint16 initialLiquidationLTVBefore;
        uint48 targetTimestampBefore;
        uint32 rampDurationBefore;
        (borrowLTVBefore, liquidationLTVBefore, initialLiquidationLTVBefore, targetTimestampBefore, rampDurationBefore) = LTVFull(collateral);


        //function call
        setLTV@withrevert(e, collateral, borrowLTV, liquidationLTV, rampDuration);
        bool reverted = lastReverted;

        //LTV values after
        uint16 borrowLTVAfter;
        uint16 liquidationLTVAfter;
        uint16 initialLiquidationLTVAfter;
        uint48 targetTimestampAfter;
        uint32 rampDurationAfter;
        (borrowLTVAfter, liquidationLTVAfter, initialLiquidationLTVAfter, targetTimestampAfter, rampDurationAfter) = LTVFull(collateral);
        uint256 nuberOfLTVsAfter = LTVList().length;
        GovernanceHarness.LTVConfig currentLtvConfigAfter = getCurrentLTVConfigHarness(collateral); 

        ///------------------------------- ASSERTS OK START----------------------
            // //collataral should not be the current contract
            // assert(collateral == currentContract => reverted, "Collateral is the current contract");

            // //borrowLTV should not be bigger than the liquidationLTV
            // assert(newBorrowLTV > newLiquidationLTV => reverted, "Borrow LTV is bigger than liquidation LTV");

            // //if the new LTV values is higher than the current LTV values and the rampDuration is bigger than 0, revert
            // assert(newLiquidationLTV >= calculatedTvl && rampDuration > 0 => reverted, "Function should revert");

            // //if the collateral was not initalized, ltvList is 1 longer
            // assert(!reverted && !isInitialized => nuberOfLTVsAfter ==  assert_uint256(nuberOfLTVsBefore +1), "Uninitalized LTV is not added to the ltvList");
            // assert(!reverted && isInitialized => nuberOfLTVsAfter == nuberOfLTVsBefore, "Initalized LTV was added to the ltvList");

            // //should not revert if non of the revert issue are met + msg.value == 0
            // assert(
            // !(collateral == currentContract) && 
            // !(newBorrowLTV > newLiquidationLTV) && 
            // !(newLiquidationLTV >= calculatedTvl && rampDuration > 0) 
            // && e.msg.value == 0 &&
            // lockedBefore == false &&
            // onBehalfeOf == governorAdmin()
            // => !reverted, "Function should not revert");

        ///------------------------------- ASSERTS OK END----------------------
        

        //if the function does not revert, the LTV values are set correctly
         assert(!reverted => 
         borrowLTVAfter == borrowLTV && 
         liquidationLTVAfter == liquidationLTV && 
         initialLiquidationLTVAfter == calculatedTvl &&
         targetTimestampAfter == assert_uint48(e.block.timestamp + rampDuration) &&
         rampDurationAfter == rampDuration &&
         currentLtvConfigAfter.initialized == true,
         "LTV values were not set correctly");

    }



//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------




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

        //when function passes, the data is set correctly
        assert(!reverted => hookTargetAfter == newHookTarget && hookedOpsAfter == wrapedHookedOps, "Hook config values were not set correctly");
        //if the hookedOps is bigger or equal to OP_MAX_VALUE, revert
        assert(hookedOps >= getOP_MAX_VALUEHarness() => reverted, "Hooked ops value is too high");

        // //should not revert if non of the revert issue are met //@audit maybe implement this later
        // assert(!(newHookTarget != 0 && selector != targetSelector ) && 
        // !(hookedOps >= getOP_MAX_VALUEHarness()) &&
        // onBehalfOf == governorAdmin() &&
        // e.msg.value == 0 &&
        // lockedBefore == false
        //  => !reverted, "Function should not revert");

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

