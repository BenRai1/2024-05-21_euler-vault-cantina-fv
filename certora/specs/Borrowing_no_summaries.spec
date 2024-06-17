import "./Base.spec";
import "./Base/borrowing_no_summaries.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;
using BorrowingHarness as BorrowingHarness;



// used to test running time
use builtin rule sanity;
// use rule privilegedOperation;

// //------------------------------- RULES TEST START ----------------------------------
//     //invarinant:
//     // 1. totalShares should be equal to sum of all user shares (+ ghosttShares that are burned in the beginning(??))


//     //touch works //@audit-check not sure how to do this since initVaultCache is private
//     rule touchWorks(env e) {
//         //VALUES BEFORE
//         require(e.block.timestamp <= max_uint48);
//         uint48 blockTimestampAsUint48 = require_uint48(e.block.timestamp);

//         //FUNCTION CALL
//         touch(e);

//         //VALUES AFTER
//           uint48 lastInterestAccumulatorUpdateAfter = BorrowingHarness.vaultStorage.lastInterestAccumulatorUpdate;


//         //ASSERTS
//         //assert1: lastInterestAccumulatorUpdate is e.block.timestamp
//         assert(lastInterestAccumulatorUpdateAfter == blockTimestampAsUint48, "lastInterestAccumulatorUpdate should be e.block.timestamp");

//         //the storage variables should be updated (lastInterestAccumulatorUpdate, accumulatedFees, totalShares, totalBOrrows, interestAccumulator)

//     }

    //repayWithShares works
    rule repayWithSharesWorks(env e){
        //@audit might require invariant for interestAccumulator
        //@audit might require invariant for totalShares
        //@audit make sure shares and owed of no other user is touched
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address onBehalfOf = actualCaller(e);
        require(onBehalfOf != receiver);
        address otherUser;
        require(otherUser != onBehalfOf && otherUser != receiver);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness(e);

        //VALUES BEFORE
        Type.Owed totalBorrowsBefore = vaultCacheBefore.totalBorrows;
        Type.Shares totalSharesBefore = vaultCacheBefore.totalShares;
        //owed
        Type.Owed owedOtherUserBefore = getCurrentOwedHarness(vaultCacheBefore,otherUser);
        Type.Owed owedOnBehalfOfBefore = getCurrentOwedHarness(vaultCacheBefore,onBehalfOf);
        Type.Owed owedReceiverBefore =  getCurrentOwedHarness(vaultCacheBefore, receiver);
        Type.Assets owedReceiverAsAssets = owedToAssetsUpHarness(e, owedReceiverBefore);
        //shares
        Type.Shares sharesOtherUserBefore = getUserSharesHarness(otherUser);
        Type.Shares sharesOnBehalfOfBefore = getUserSharesHarness(onBehalfOf);
        Type.Shares sharesReceiverBefore = getUserSharesHarness(receiver);

        //final Values
        Type.Shares finalSharesToRepay;
        Type.Assets finalAssetsToRepay;
        finalSharesToRepay, finalAssetsToRepay = repayWithSharesCalculationHarness(e, amount, sharesOnBehalfOfBefore, vaultCacheBefore, owedReceiverAsAssets); 
        Type.Owed finalOwedToRepay = assetsToOwedHarness(e, finalAssetsToRepay);


        //FUNCTION CALL
        repayWithShares(e, amount, receiver);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness(e);
        Type.Shares totalSharesAfter = vaultCacheAfter.totalShares;
        Type.Owed totalBorrowsAfter = vaultCacheAfter.totalBorrows;
        Type.Owed owedOtherUserAfter = getCurrentOwedHarness(vaultCacheAfter,otherUser);
        Type.Owed owedOnBehalfOfAfter = getCurrentOwedHarness(vaultCacheAfter,onBehalfOf);
        Type.Owed owedReceiverAfter =  getCurrentOwedHarness(vaultCacheAfter, receiver);
        Type.Shares sharesOtherUserAfter = getUserSharesHarness(otherUser);
        Type.Shares sharesOnBehalfOfAfter = getUserSharesHarness(onBehalfOf);
        Type.Shares sharesReceiverAfter = getUserSharesHarness(receiver);




        //ASSERTS
        // //assert1: OwedReceiverAsAssets != 0 => sharesOnBehalfOfAfter == sharesOnBehalfOfBefore - finalSharesToRepay
        // assert(owedReceiverAsAssets != 0 => to_mathint(sharesOnBehalfOfAfter) == sharesOnBehalfOfBefore - finalSharesToRepay, "Should decrease user shares");

        // //assert2: OwedReceiverAsAssets != 0 => totalSharesAfter == totalSharesBefore - finalSharesToRepay
        // assert(owedReceiverAsAssets != 0 => to_mathint(totalSharesAfter) == totalSharesBefore - finalSharesToRepay, "Should decrease total shares");

        // //assert3: OwedReceiverAsAssets != 0 => totalBorrowsAfter == totalBorrowsBefore - finalOwedToRepay
        // assert(owedReceiverAsAssets != 0 => to_mathint(totalBorrowsAfter) == totalBorrowsBefore - finalOwedToRepay, "Should decrease total borrows");

        // //assert4: OwedReceiverAsAssets != 0 => owedReceiverAfter == owedReceiver - finalOwedToRepay
        // assert(owedReceiverAsAssets != 0 => to_mathint(owedReceiverAfter) == owedReceiverBefore - finalOwedToRepay, "Should decrease user owed");

        //assert8: sharesReceiverAfter == sharesReceiverBefore
        // assert(sharesReceiverAfter == sharesReceiverBefore, "Should not change receiver shares");

        // //assert9: owedOnBehalfOfAfter == owedOnBehalfOfBefore
        // assert(owedOnBehalfOfAfter == owedOnBehalfOfBefore, "Should not change on behalf of user owed");

        //---------------------Asserts OK START----------------------

            //assert5: owedOtherUserAfter == owedOtherUserBefore
            assert(owedOtherUserAfter == owedOtherUserBefore, "Should not change other user owed");

            //assert6: sharesOtherUserAfter == sharesOtherUserBefore
            assert(sharesOtherUserAfter == sharesOtherUserBefore, "Should not change other user shares");

        //---------------------Asserts OK END----------------------

    }   



//     //only should increase usershares //@audit passes but should not pass since pullDebt does not touch shares
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
        f.selector == sig:borrow(uint256,address).selector ||
        f.selector == sig:pullDebt(uint256, address).selector, 
        "Should increase user shares");
    } 



// //------------------------------- RULES TEST END ----------------------------------

// //------------------------------- RULES PROBLEMS START ----------------------------------



    //only should decrease user shares //@audit timeout for pullDebt
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
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:pullDebt(uint256, address).selector || 
        f.selector == sig:repayWithShares(uint256, address).selector, 
        "Should not decrease user shares");
    }

    //repayWithShares reverts //@audit timeout for assert4
    rule repayWithSharesReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = CVLUpdateVault();
        bool isController = vaultIsController(onBehalfOf);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness(e);
        Type.Owed owedReceiver =  getCurrentOwedHarness(vaultCacheBefore, receiver);
        Type.Assets OwedReceiverAsAssets = owedToAssetsUpHarness(e, owedReceiver);
        Type.Shares sharesOnBehalfOf = getUserSharesHarness(onBehalfOf);

        //Calculating amount to repay
        Type.Shares sharesToRepay;
        Type.Assets assetsToRepay;

        sharesToRepay, assetsToRepay = repayWithSharesCalculationHarness(e, amount, sharesOnBehalfOf, vaultCache, OwedReceiverAsAssets); 


        //VALUES BEFORE
        bool isRepayWithSharesDisabled = isRepayWithSharesDisabled(e);

        //FUNCTION CALL
        repayWithShares@withrevert(e, amount, receiver);
        bool lastRevert = lastReverted;

        //VALUES AFTER

        //ASSERTS



        // //assert3: if sharesOnBehalfOf < sharesToRepay, then revert
        // assert(sharesOnBehalfOf < sharesToRepay => lastRevert, "Not enough shares available to repay");

        // //assert4: if owed is less than assetsToRepay, then revert
        // assert(to_mathint(OwedReceiverAsAssets) < to_mathint(assetsToRepay) => lastRevert, "Not enough owed to repay");

        //---------------ASSERTS OK START----------------

        //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => lastRevert, "Only EVC can call repayWithShares");

        //assert2: if onBehalfOf is address(0), then revert
        assert(onBehalfOf == 0 => lastRevert, "On behalf of should not be address(0)");

        //assert5: if isRepayWithSharesDisabled, then revert
        // assert(isRepayWithSharesDisabled => lastRevert, "RepayWithShares should not be disabled");



        //---------------ASSERTS OK END----------------

    }

    //only should reduce owed/debt //@audit timeout for repay
    rule onlyReduceOwed(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Owed owedBefore = getOwedHarness(user);
        requireInvariant vaultInterAccumGreaterOrEqualUserInterAccum(e,user);


        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = getOwedHarness(user);

        //ASSERTS
        assert(owedAfter < owedBefore =>
        f.selector == sig:pullDebt(uint256, address).selector ||
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector,
        "Should not reduce user owed");
    }

    //only should increase owed/debt //@audit timeout for repayWithShares and error for repay (repay 0 and increase borrow becasue of interest)
    rule onlyIncreaseOwed(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Owed owedBefore = getOwedHarness(user);
        requireInvariant vaultInterAccumGreaterOrEqualUserInterAccum(e,user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = getOwedHarness(user);

        //ASSERTS
        assert(owedAfter > owedBefore =>
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector ||
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:pullDebt(uint256, address).selector,
        "Should not increase user owed");
    }

    //only should increase total borrows //@audit timeout for repayWithShares and error for repay (repay 0 and increase borrow becasue of interest)
    rule onlyIncreaseTotalBorrows(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        Type.Owed totalBorrowsBefore = getTotalBorrowsHarness();

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed totalBorrowsAfter = getTotalBorrowsHarness();

        //ASSERTS
        assert(totalBorrowsAfter > totalBorrowsBefore =>
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector ||
        f.selector == sig:borrow(uint256, address).selector,
        "Should not increase total borrows");
    }



// //------------------------------- RULES PROBLEMS END ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    //only change user shares 
    rule onlyChangeUserShares(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Shares userSharesBefore = getUserSharesHarness(user);
        requireInvariant vaultInterAccumGreaterOrEqualUserInterAccum(e,user);


        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares userSharesAfter = getUserSharesHarness(user);

        //ASSERTS
        assert(userSharesAfter != userSharesBefore =>
        f.selector == sig:repayWithShares(uint256, address).selector, "Should not change user shares");
    }

    //touch reverts
    rule touchReverts(env e) {
        //FUNCTION PARAMETER
        address onBehalfOf = actualCaller(e);
        // bool isTouchDisabled = isTouchDisabled(e);

        //FUNCTION CALL
        touch@withrevert(e);
        bool lastRevert = lastReverted;

        //ASSERTS
        //assert1: if onBehalfOf = 0, then revert
        assert(onBehalfOf == 0 => lastRevert, "On behalf of should not be address(0)");

        //assert2: if e.msg.sender != evc, then revert
        assert(EVC != e.msg.sender => lastRevert, "Only EVC can call touch");

        //assert3: if isTouchDisabled, then revert
        // assert(isTouchDisabled => lastRevert, "Touch should not be disabled");
    }

    //flashloan reverts
    rule flashLoanReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        bytes data;

        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = CVLUpdateVault();

        //VALUES BEFORE
        uint vaultBalanceBefore = getUserCollateralBalanceHarness(vaultCache,currentContract);
        // bool isFlashLoanDisabled = isFlashLoanDisabled(e);

        //FUNCTION CALL
        flashLoan@withrevert(e, amount, data);
        bool lastRevert = lastReverted;

        //VALUES AFTER
        uint vaultBalanceAfter = getUserCollateralBalanceHarness(vaultCache,currentContract);

        //ASSERTS
        //assert1: if onBehalfOf = 0, then revert
        assert(onBehalfOf == 0 => lastRevert, "On behalf of should not be address(0)");

        //assert2: vaultBalanceAfter < vaultBalanceBefore, then revert
        assert(vaultBalanceAfter < vaultBalanceBefore => lastRevert, "Vault balance should not decrease");

        //assert3: if isFlashLoanDisabled, then revert
        // assert(isFlashLoanDisabled => lastRevert, "FlashLoan should not be disabled"); 
    }

    //only changes total borrows
    rule onlyChangeTotalBorrows(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        Type.Owed totalBorrowsBefore = getTotalBorrowsHarness();

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed totalBorrowsAfter = getTotalBorrowsHarness();

        //ASSERTS
        assert(totalBorrowsAfter != totalBorrowsBefore =>
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector,
        "Should change total borrows");
    }

    //only should decrease total borrows
    rule onlyDecreaseTotalBorrows(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        Type.Owed totalBorrowsBefore = getTotalBorrowsHarness();

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed totalBorrowsAfter = getTotalBorrowsHarness();

        //ASSERTS
        assert(totalBorrowsAfter < totalBorrowsBefore =>
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector,
        "Should not decrease total borrows");
    }

    //only change user owed
    rule onlyChangeUserOwed(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        Type.Owed owedBefore = getOwedHarness(user);
        requireInvariant vaultInterAccumGreaterOrEqualUserInterAccum(e,user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Owed owedAfter = getOwedHarness(user);

        //ASSERTS
        assert(owedAfter < owedBefore =>
        f.selector == sig:pullDebt(uint256, address).selector ||
        f.selector == sig:repay(uint256, address).selector ||
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:repayWithShares(uint256, address).selector,
        "Should not reduce user owed");
    }
   
    //only should reduce assets(underlying) held by user
    rule onlyReduceUserAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        require(user != currentContract);
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, user);

        //ASSERTS
        assert(assetsAfter < assetsBefore =>
        f.selector == sig:repay(uint256, address).selector,
        "Should not reduce user assets");
    }

    //only should increase assets(underlying) held by user
    rule onlyIncreaseUserAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address user;
        require(user != currentContract);
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, user);

        //ASSERTS
        assert(assetsAfter > assetsBefore =>
        f.selector == sig:borrow(uint256, address).selector,
        "Should not increase user assets");
    }

    //only should reduce assets(underlying) held by vault
    rule onlyReduceVaultAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address vault;
        require(vault == currentContract);
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, vault);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, vault);

        //ASSERTS
        assert(assetsAfter < assetsBefore =>
        f.selector == sig:borrow(uint256, address).selector,
        "Should not increase user assets");
    }

    //only should increase assets(underlying) held by vault
    rule onlyIncreaseVaultAssets(env e, method f, calldataarg args) filtered{f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)}{
        //FUNCTION PARAMETER
        address vault;
        require(vault == currentContract);
        Type.VaultCache vaultCache = CVLUpdateVault();
        uint256 assetsBefore = getUserCollateralBalanceHarness(vaultCache, vault);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = getUserCollateralBalanceHarness(vaultCache, vault);

        //ASSERTS
        assert(assetsAfter > assetsBefore =>
        f.selector == sig:repay(uint256, address).selector,
        "Should not reduce user assets");
    }  


//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------
    //invariants: global interest accumulater should always be greater or eaqual to the user interestaccumulater
    invariant vaultInterAccumGreaterOrEqualUserInterAccum(env e, address user) 
        getUserInterestAccExt(e, user) <= getVaultInterestAccExt(e)
        filtered {
        f -> !BASE_HARNESS_FUNCTIONS(f) && !BORROWING_HARNESS_FUNCTIONS(f)
    }

//------------------------------- INVARIENTS OK END-------------------------------

