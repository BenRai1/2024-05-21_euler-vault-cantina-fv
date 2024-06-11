import "./Base.spec";
import "./Base/borrowing_no_summaries.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;
using BorrowingHarness as BorrowingHarness;



// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//------------------------------- RULES TEST START ----------------------------------

    //only should change increase usershares
    rule onlyIncreaseUserShares(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Shares userSharesBefore = getUserSharesHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares userSharesAfter = getUserSharesHarness(user);

        //ASSERTS
        assert(userSharesAfter > userSharesBefore =>
        f.selector == sig:pullDebt(uint256, address).selector ||
        f.selector == sig:borrow(uint256, address).selector, "Should increase user shares");
    } 

    //only should decrease user shares
    rule onlyDecreaseUserShares(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Shares userSharesBefore = getUserSharesHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares userSharesAfter = getUserSharesHarness(user);

        //ASSERTS
        assert(userSharesAfter < userSharesBefore =>
        f.selector == sig:repayWithShares(uint256, address).selector, "Should decrease user shares");
    }

    //only should reduce owed/debt
    rule onlyReduceOwed(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Owed owedBefore = getOwedHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = getOwedHarness(user);

        //ASSERTS
        assert(owedAfter < owedBefore =>
        f.selector == sig:pullDebt(uint256, address).selector ||
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector,
        "Should reduce owed");
    }

    //only should increase owed/debt
    rule onlyIncreaseOwed(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Owed owedBefore = getOwedHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = getOwedHarness(user);

        //ASSERTS
        assert(owedAfter > owedBefore =>
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:pullDebt(uint256, address).selector,
        "Should increase owed");
    }

    //only should reduce assets(underlying) held by user
    rule onlyReduceAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, user);

        //ASSERTS
        assert(assetsAfter < assetsBefore =>
        f.selector == sig:repay(uint256, address).selector,
        "Should reduce user assets");
    }

    //only should increase assets(underlying) held by user
    rule onlyIncreaseAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, user);

        //ASSERTS
        assert(assetsAfter > assetsBefore =>
        f.selector == sig:borrow(uint256, address).selector,
        "Should increase user assets");
    }





    //repayWithShares reverts
    rule repayWithSharesReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = CVLUpdateVault();
        bool isController = vaultIsController(onBehalfOf);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness(e);
        BorrowingHarness.Owed owedReceiver =  getCurrentOwedHarness(vaultCacheBefore, receiver);
        Type.Assets OwedReceiverAsAssets = owedToAssetsUpHarness(e, owedReceiver);
        Type.Shares sharesOnBehalfOf = getUserSharesHarness(onBehalfOf);

        //Calculating amount to repay
        Type.Shares sharesToRepay;
        Type.Assets assetsToRepay;

        sharesToRepay, assetsToRepay = repayWithSharesCalculationHarness(e, amount, sharesOnBehalfOf, vaultCache, OwedReceiverAsAssets); 


        //VALUES BEFORE

        //FUNCTION CALL
        repayWithShares@withrevert(e, amount, receiver);
        bool lastRevert = lastReverted;

        //VALUES AFTER

        //ASSERTS



        // //assert3: if sharesOnBehalfOf < sharesToRepay, then revert
        // assert(sharesOnBehalfOf < sharesToRepay => lastRevert, "Not enough shares available to repay");

        //assert4: if owed is less than assetsToRepay, then revert
        assert(to_mathint(owedReceiver) < to_mathint(assetsToRepay) => lastRevert, "Not enough owed to repay");

        //---------------ASSERTS OK START----------------

        // //assert1: if e.msg.sender is not evc, then revert
        // assert(EVC != e.msg.sender => lastRevert, "Only EVC can call repayWithShares");

        // //assert2: if onBehalfOf is address(0), then revert
        // assert(onBehalfOf == 0 => lastRevert, "On behalf of should not be address(0)");



        //---------------ASSERTS OK END----------------

    }


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
