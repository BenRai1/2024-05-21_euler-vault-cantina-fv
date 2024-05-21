import "./Base.spec";
import "./Base/governance.spec";



// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//------------------------------- RULES TEST START ----------------------------------



    //setCaps works
    rule setCapsIntegraty(env e) {
        uint16 cap1;
        uint16 cap2;
        
        //function call
        setCaps(e, cap1, cap2);
        
        //caps values after
        uint16 cap1After;
        uint16 cap2After;
        (cap1After, cap2After) = caps();

        assert(cap1After == cap1 && cap2After == cap2, "Caps values were not set correctly");
    }

    //setInterestFee works //@audit-issue Vault must be updated first, must be in the range
    rule setInterestFeeIntegraty(env e) {
        uint16 interestFee;

        //function call
        setInterestFee(e, interestFee);

        //interestFee value after
        uint16 interestFeeAfter = interestFee();

        assert(interestFeeAfter == interestFee, "Interest fee was not set correctly");
    }

    //setInterestRateModel works //@audit-issue Vault must be updated first, must be in the range
    rule setInterestRateModelIntegraty(env e) {
        address interestRateModel;

        //function call
        setInterestRateModel(e, interestRateModel);

        //interestRateModel value after
        address interestRateModelAfter = interestRateModel();

        assert(interestRateModelAfter == interestRateModel, "Interest rate model was not set correctly");
    }


    //setLTV works //@audit-issue check if the address is "itslef"
    rule setLTVIntegraty(env e) {
        address collateral;
        uint16 borrowLTV;
        GovernanceHarness.ConfigAmount newBorrowLTV = toConfigAmountHarness(borrowLTV);
        uint16 liquidationLTV;
        GovernanceHarness.ConfigAmount newLiquidationLTV = toConfigAmountHarness(liquidationLTV);
        uint32 rampDuration;

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

        // assert(borrowLTVAfter == borrowLTV && liquidationLTVAfter == liquidationLTV && rampDurationAfter == rampDuration, "LTV values were not set correctly");


        //------------------------------- ASSERTS OK ----------------------

        // //collataral should not be the current contract
        // assert(collateral == currentContract => reverted, "Collateral is the current contract");

        // //borrowLTV should not be bigger than the liquidationLTV
        // assert(newBorrowLTV > newLiquidationLTV => reverted, "Borrow LTV is bigger than liquidation LTV");


    }



 //------------------------------- TESTING ----------------------------------

    // Spesific state variables can only be changed by the governor
    rule onlyGovernorCanChangeStateVariables(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure}{
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



    //setHookConfig works
    rule setHookConfigIntegraty(env e) {
        address hookTarget;
        uint32 hookedOps;

        //function call
        setHookConfig@withrevert(e, hookTarget, hookedOps);
        bool reverted = lastReverted;

        //hookConfig values after
        address hookTargetAfter;
        uint32 hookedOpsAfter;
        (hookTargetAfter, hookedOpsAfter) = hookConfig();

        assert(!lastReverted => hookTargetAfter == hookTarget && hookedOpsAfter == hookedOps, "Hook config values were not set correctly");
        assert(hookedOps >= getOP_MAX_VALUEHarness() => reverted, "Hooked ops value is too high");
    }

//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------





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

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

