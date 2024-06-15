import "./Base.spec";
import "./Base/riskManager.spec";
import "./Base/abstractBase.spec";
using EthereumVaultConnector as EVC;
// using EVault as EVault;


// used to test running time
use builtin rule sanity;
// use rule privilegedOperation;


//------------------------------- RULES OK START ------------------------------------

    //function needs to revert if nonReentrantView modifier reverts
    rule nonReentrantViewModifier(env e, method f, calldataarg arg) filtered{f->
        f.selector == sig:accountLiquidity(address,bool).selector ||
        f.selector == sig:accountLiquidityFull(address,bool).selector}{
        //VALUES BEFORE
        bool reentrancyLocked = reentrancyLockedHarness();
        address hookTarget = getHookTargetHarness();
        address msgSender = e.msg.sender;
        address viewCaller = useViewCallerHarness();

        //FUNCTION CALL
        f@withrevert(e,arg);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if reentrancyLocked is true, msg.sender is not hookTarget and msg.sender = currentContract and viewCaller == hookTarget, the function should revert
        assert(reentrancyLocked && msgSender != hookTarget && !(msgSender == currentContract && viewCaller == hookTarget) => reverted, "Function should revert");
    }

    //only spesific functions should change snapshot 
    rule onlyChangeSnapshot(env e, method f, calldataarg arg) filtered{f->
        !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !HARNESSES_FUNCTIONS(f)}{
        //VALUES BEFORE
        RiskManagerHarness.Snapshot snapshotBefore = getSnapshotHarness();

        //FUNCTION CALL 
        f(e, arg);

        //VALUES AFTER
        RiskManagerHarness.Snapshot snapshotAfter = getSnapshotHarness();

        //ASSERTS
        //assert1: if snapshotBefore != snapshotAfter, the called function should be checkVaultStatus
        assert(snapshotBefore != snapshotAfter => f.selector == sig:checkVaultStatus().selector, "Function should be checkVaultStatus"); 
    }

    //only spesific functions should change if the controller is enabled
    rule onlyChangeDisableController(env e, method f, calldataarg arg) filtered{f->
        !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !HARNESSES_FUNCTIONS(f)}{
        //VALUES BEFORE
        address account;
        bool isEnabledBefore = EVC.isControllerEnabled(e, account, currentContract);

        //FUNCTION CALL 
        f(e, arg);

        //VALUES AFTER
        bool isEnabledAfter = EVC.isControllerEnabled(e, account, currentContract);

        //ASSERTS
        //assert1: if isEnabledBefore != isEnabledAfter, the called function should be disableController
        assert(isEnabledBefore != isEnabledAfter => f.selector == sig:disableController().selector, "Function should be disableController"); 
    }

    //function needs to revert if reentrancyLocked is true
    rule reentrancyLockedModifier(env e, method f, calldataarg arg) filtered{f->
        f.selector == sig:disableController().selector}{
        //VALUES BEFORE
        bool reentrancyLocked = reentrancyLockedHarness();

        //FUNCTION CALL
        f@withrevert(e,arg);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if reentrancyLocked is true, the function should revert
        assert(reentrancyLocked => reverted, "Function should revert");
    }

    //functions need to revert if onlyEVCChecks modifier reverts
    rule onlyEVCChecksModifier(env e, method f, calldataarg arg) filtered{f->
        f.selector == sig:checkAccountStatus(address,address[]).selector ||
        f.selector == sig:checkVaultStatus().selector}{
        //VALUES BEFORE
        address msgSender = e.msg.sender;
        bool evcChecksInProgress = EVC.areChecksInProgress(e);
        
        //FUNCTION CALL
        f@withrevert(e,arg);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if msg.sender is not evc or evcChecksInProgress is false, the function should revert
        assert(msgSender != evc || !evcChecksInProgress => reverted, "Function should revert");
    }

    //checkVaultStatus works
    rule checkVaultStatusIntegraty(env e) {
        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        bool snapshotInitalizedBefore = vaultCacheBefore.snapshotInitialized;
        RiskManagerHarness.Snapshot snapshotBefore = getSnapshotHarness();
        bytes4 magicValueTarget = toBytes4Harness(e, sig:checkVaultStatus().selector);
        address irm = currentContract.vaultStorage.interestRateModel;
        uint72 interestRateBefore = currentContract.vaultStorage.interestRate;
        uint256 ghostInterestRate = GhostCalculatedInterestRate[currentContract];
        uint72 calculatedInterestRate = assert_uint72(calculateInterestRateHarness(e, ghostInterestRate));

        //FUNCTION CALL
        bytes4 returnedSelectorCall = checkVaultStatus(e);

        //VALUES AFTER
        RiskManagerHarness.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        bool snapshotInitalizedAfter = vaultCacheAfter.snapshotInitialized;
        RiskManagerHarness.Snapshot snapshotAfter = getSnapshotHarness();
        uint72 interestRateAfter = currentContract.vaultStorage.interestRate;

        //ASSERTS
        //assert1: the returned selector is the right one
        assert(returnedSelectorCall == magicValueTarget, "Returned selector does not match");

        //assert2: if snapshot is initialized, at the end it is no longer initialized
        assert(snapshotInitalizedBefore => !snapshotInitalizedAfter, "Snapshot is still initialized");

        //assert3: if snapshot is initialized, at the end snapshot.cash and snapshot.borrows are equal to 0
        assert(snapshotInitalizedBefore => toUintHarness(snapshotAfter.cash) == 0 && toUintHarness(snapshotAfter.borrows) == 0, "Snapshot cash and borrows are not 0");

        //assert4: if irm is address(0), interest rate stays the same
        assert(irm == 0 => interestRateBefore == interestRateAfter, "Interest rate changed");

        //assert5: vaultStorage.initeresRate is equal to calculated interest rate
        assert(irm != 0 => interestRateAfter == calculatedInterestRate, "Interest rate does not match");
    }

    //checkVaultStatus reverts
    rule checkVaultStatusReverts(env e) {
        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        bool snapshotInitalizedBefore = vaultCacheBefore.snapshotInitialized;
        RiskManagerHarness.Snapshot snapshotBefore = getSnapshotHarness();
        RiskManagerHarness.Owed totalBorrowsBefore = vaultCacheBefore.totalBorrows;
        RiskManagerHarness.Assets calculatedBorrows = toAssetUPHarness(totalBorrowsBefore);
        uint256 borrows = toUintHarness(calculatedBorrows);
        uint256 prevBorrows = toUintHarness(snapshotBefore.borrows);
        uint256 prevSupply = assert_uint256(toUintHarness(snapshotBefore.cash)+ prevBorrows);
        uint256 supply = totalAssetsHarness(vaultCacheBefore);
        bool isCheckVaultStatusDisabled = isVaultStatusCheckDisabled(e);

        //FUNCTION CALL
        checkVaultStatus@withrevert(e);
        bool reverted = lastReverted;

        //VALUES AFTER
        RiskManagerHarness.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        bool snapshotInitalizedAfter = vaultCacheAfter.snapshotInitialized;

        //ASSERTS
        //assert1: if snapshot is initialized, borrow is bigger than borrowCap and borrow > prevBorrows, the function reverts
        assert(snapshotInitalizedBefore && borrows > vaultCacheBefore.borrowCap && borrows > prevBorrows => reverted, "Borrows is bigger than borrowCap and prevBorrows");

        //assert2: if snapshot is initialized, supply > supplyCap and supply > prevSupply, the function reverts
        assert(snapshotInitalizedBefore && supply > vaultCacheBefore.supplyCap && supply > prevSupply => reverted, "Supply is bigger than supplyCap and prevSupply");

        //assert3: if isCheckVaultStatusDisabled, the function reverts
        assert(isCheckVaultStatusDisabled => reverted, "CheckVaultStatus is disabled");
    }

    //accountLiquidityFull works
    rule accountLiquidityFullIntegrity(env e) {
        //CALL PARAMETER
        address account;
        bool liquidation;

        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address[] controllers = EVC.getControllers(e, account);
        RiskManagerHarness.Owed owed = getOwedHarness(account);
        uint256 liabilityValueCalculated = getLiabilityValueHarness(e, vaultCache, account, owed, liquidation);
        address[] collaterals = EVC.getCollaterals(e, account);
        require(collaterals.lenght < 3);
        uint256 i;
        require(i < collaterals.lenght);
        uint256 j;
        require(j < collaterals.lenght);
        uint256[] collateralValuesCalculated = getCollateralValuesHarness(e, vaultCache, account, collaterals, liquidation);

        //FUNCTION CALL
        address[] collateralsCall;
        uint256[] collateralValuesCall;
        uint256 liabilityValueCall;
        (collateralsCall, collateralValuesCall, liabilityValueCall) = accountLiquidityFull(e, account, liquidation);

        //ASSERTS
        //assert1: collaterals == collateralsCall && collateralValuesCall = collateralValuesCalculated && liabilityValueCall = liabilityValueCalculated
        assert(collaterals[i] == collateralsCall[i] && 
        collateralValuesCall[j] == collateralValuesCalculated[j] && liabilityValueCall == liabilityValueCalculated, 
        "Returned values do not match");
    }

    //accountLiquidityFull reverts
    rule accountLiquidityFullReverts(env e) {
        //CALL PARAMETER
        address account;
        bool liquidation;

        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address[] controllers = EVC.getControllers(e, account);

        //FUNCTION CALL
        accountLiquidityFull@withrevert(e, account, liquidation);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert1: if controllers.length > 1, the function reverts
        assert(controllers.length > 1 => reverted, "Controllers length is greater than 1");

        //assert2: if controllers.length == 0, the function reverts
        assert(controllers.length == 0 => reverted, "Controllers length is 0");

        //assert3: if controller[0] != currentContract, the function reverts
        assert(controllers[0] != currentContract => reverted, "Controller is not currentContract");

        //assert4: if orracle is address(0), the function reverts
        assert(vaultCache.oracle == 0 => reverted, "Oracle is address(0)");
    }

    //accountLiquidity reverts
    rule accountLiquidityReverts(env e) {
        //CALL PARAMETER
        address account;
        bool liquidation;

        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address[] controllers = EVC.getControllers(e, account);

        //FUNCTION CALL
        accountLiquidity@withrevert(e, account, liquidation);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert1: if controllers.length > 1, the function reverts
        assert(controllers.length > 1 => reverted, "Controllers length is greater than 1");

        //assert2: if controllers.length == 0, the function reverts
        assert(controllers.length == 0 => reverted, "Controllers length is 0");

        //assert3: if controller[0] != currentContract, the function reverts
        assert(controllers[0] != currentContract => reverted, "Controller is not currentContract");

        //assert4: if orracle is address(0), the function reverts
        assert(vaultCache.oracle == 0 => reverted, "Oracle is address(0)");
    }

    //accountLiquidity works
    rule accountLiquidityIntegrity(env e) {
        //CALL PARAMETER
        address account;
        bool liquidation;

        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address[] controllers = EVC.getControllers(e, account);
        RiskManagerHarness.Owed owed = getOwedHarness(account);
        uint256 liabilityValueCalculated = getLiabilityValueHarness(e, vaultCache, account, owed, liquidation);
        address[] collaterals = EVC.getCollaterals(e, account);
        require(collaterals.lenght < 3);
        uint256 collateralValueCalculated = getCollateralValueHarness(e, vaultCache, account, collaterals, liquidation);

        //FUNCTION CALL
        uint256 collateralValueCall;
        uint256 liabilityValueCall;
        (collateralValueCall, liabilityValueCall) = accountLiquidity(e, account, liquidation);

        //ASSERTS
        //assert1: collateralValueCall = collateralValueCalculated && liabilityValueCall = liabilityValueCalculated
        assert(collateralValueCall == collateralValueCalculated && liabilityValueCall == liabilityValueCalculated, "Returned values do not match");
    }

    //checkAccountStatus works + reverts
    rule checkAccountStatusIntegraty(env e) {
        //CALL PARAMETER
        address account;
        address[] collaterals;
        require(collaterals.lenght < 3);
        bytes4 magicValueTarget = toBytes4Harness(e, sig:checkAccountStatus(address, address[]).selector);

        //VALUES BEFORE
        RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        RiskManagerHarness.Owed owed = getOwedHarness(account);
        uint256 liabilityValue = getLiabilityValueHarness(e, vaultCache, account, owed, false);
        uint256 collateralValue = getCollateralValueHarness(e, vaultCache, account, collaterals, false);

        //FUNCTION CALL
        bytes4 magicValueCall = checkAccountStatus@withrevert(e, account, collaterals);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if oracle is address(0), the function reverts
        assert(owed != 0 && vaultCache.oracle == 0 => reverted, "Oracle is address(0)so functin should revert");

        //assert2: if !(collateralValue > liabilityValue), function reverts
        assert(owed != 0 && !(collateralValue > liabilityValue) => reverted, "Collateral value is not greater than liability value");

        //assert3: if not reverted, the function returns the magic value
        assert(owed != 0 && !reverted => magicValueCall == magicValueTarget, "Magic value does not match");

        // //assert4: should not revert if collateralValue > liabilityValue and oracle is not address(0)
        // assert(collateralValue > liabilityValue && vaultCache.oracle != 0 && e.msg.value == 0 && (e.msg.sender == evc || EVC.areChecksInProgress(e)) => !reverted, "Function should not revert"); //@audit reverts but no reason is given in the job
    }

    //disableController works
    rule disableControllerIntegraty(env e) {
        //CALL PARAMETER
        address account = actualCaller(e);

        //VALUES BEFORE
        RiskManagerHarness.Owed owedBefore = getOwedHarness(account);
        address[] controllers = EVC.getControllers(e, account); 
        uint8 numberOfElementsBefore = EVC.accountCollaterals[account].numElements;
        require(numberOfElementsBefore == 1);
        uint256 lengthElementsBefore = EVC.getControllers(e, account).length;
        require(lengthElementsBefore == 1);

        //FUNCTION CALL
        disableController@withrevert(e);
        bool reverted = lastReverted;

        //VALUES AFTER
        bool isEnabledAfter = EVC.isControllerEnabled(e, account, currentContract);

        //ASSERTS
        //assert1: revert if account does not owe anything
        assert(owedBefore != 0 => reverted, "Account is still owing something");

        //assert2: if not reverted, the controller is disabled after
        assert(!reverted => !isEnabledAfter, "Controller is still enabled");
    }

//------------------------------- RULES OK END ------------------------------------