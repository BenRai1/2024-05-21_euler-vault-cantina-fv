import "./Base.spec";
import "./Base/borrowing.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;
using BorrowingHarness as BorrowingHarness;



// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants: 
//- interestAccumulator of a user account is never bigger than the global interestAccumulator
//- total borrows is always equal to the sum of all borrows

//------------------------------- RULES TEST START ----------------------------------






//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------




//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    //nonReentrantView modifier works
    rule nonReentrantViewWorks(env e, method f, calldataarg args) filtered{
        f-> NONREENTRANTVIEW_FUNCTIONS(f)
    }{
        //VALUES BEFORE
        bool reentrancyLocked = BorrowingHarness.vaultStorage.reentrancyLocked;
        address hookTarget = BorrowingHarness.vaultStorage.hookTarget;
        bool shouldRevert = e.msg.sender != hookTarget && !(e.msg.sender == currentContract && CVLuseViewCaller() == hookTarget);

        //FUNCTION CALL
        f@withrevert(e, args);
        bool reverted = lastReverted;

        //ASSERTS
        assert(reentrancyLocked && shouldRevert => reverted, "Function call should revert");
    }

    //only functions to change vaultStorage cash
    rule onlyToChangeVaultStorageCash(env e, method f, calldataarg args) filtered{
        f -> !f.isView && !f.isPure 
        && !BASE_HARNESS_FUNCTIONS(f)
        && !BORROWING_HARNESS_FUNCTIONS(f)
    } {
        //VALUES BEFORE
        uint256 cashBefore = cash(e);

        //FUNCTION CALL
        f(e,args);

        //VALUES AFTER
        uint256 cashAfter = cash(e);

        //ASSERTION
        assert(cashBefore != cashAfter => 
        f.selector == sig:borrow(uint256, address).selector ||
        f.selector == sig:repay(uint256, address).selector,
        "Functions should not be able to change cash");
    }

    //borrow Reverts work
    rule borrowReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        BorrowingHarness.Assets amountAsAssests = uintToAssetsHarness(e, amount);
        address receiver;
        address onBehalfOf = actualCaller(e);

        //VALUES BEFORE
        BorrowingHarness.VaultCache vaultCacheBefore = CVLUpdateVault();
        BorrowingHarness.Assets cashBefore = BorrowingHarness.vaultStorage.cash;
        BorrowingHarness.Assets targetAmountAsAssets = 
            amount == max_uint256 ? 
            cashBefore : 
            amountAsAssests;
        bool vaultIsController = vaultIsController(onBehalfOf);
        bool isNotSet = isNotSetCompatibeAssetHarness(vaultCacheBefore.configFlags);
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(receiver);
        bool isBorrowDisabled = isBorrowDisabled(e);
 
        //function call
        borrow@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
         //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => reverted, "Only EVC can call pullDebt");

        //assert2: if onBehalfOf is 0, then revert
        assert(onBehalfOf == 0 => reverted, "On behalf of should not be address(0)");

        //assert3: if vault not controller, then revert
        assert(!vaultIsController => reverted, "Vault needs to be controller");

        //assert4: if assets > vaultCache.cash, then revert
        assert(targetAmountAsAssets > cashBefore => reverted, "Amount should not be greater than the vault cash");

        //assert5: if receiver is 0, then revert
        assert(amountAsAssests != 0 => receiver == 0 => reverted, "Receiver should not be address(0)");

        //assert6: if configflag is not set and isKnownNonOwnerAccount(receiver), then revert
        assert(amountAsAssests != 0 => isNotSet && isKnownNonOwnerAccount => reverted, "Config flag should be set and receiver should not be a known non owner account");

        //assert7: if borrow is disabled, then revert
        assert(isBorrowDisabled => reverted, "Borrow should not be disabled");
    }

    //borrow works
    rule borrowIntegraty(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        BorrowingHarness.Assets amountAsAssests = uintToAssetsHarness(e, amount);
        address receiver;
        require(receiver != currentContract);
        address onBehalfOf = actualCaller(e);
        require(onBehalfOf != currentContract);
        address otherUser;
        require(otherUser != receiver && otherUser != currentContract && otherUser != onBehalfOf);
        BorrowingHarness.VaultCache vaultCacheBefore = CVLUpdateVault();
        BorrowingHarness.Assets cashBefore = BorrowingHarness.vaultStorage.cash;
        require(vaultCacheBefore.asset == VaultAsset);
        BorrowingHarness.Assets targetAmountAsAssets = 
            amount == max_uint256 ? 
            cashBefore : 
            amountAsAssests;
        BorrowingHarness.Owed targetAmountAsOwed = assetsToOwedHarness(e,targetAmountAsAssets);  

        //VALUES BEFORE
        //balances before
        uint256 balanceReceiverBefore = VaultAsset.balanceOf(e, receiver);
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e, currentContract);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e, otherUser);
        //owed before
        BorrowingHarness.Owed owedOnBehalfOfBefore = CVLGetCurrentOwed(onBehalfOf);
        BorrowingHarness.Owed owedOtherUserBefore = CVLGetCurrentOwed(otherUser);
        uint256 totalBorrowsBefore = BorrowingHarness.vaultStorage.totalBorrows;

        //FUNCTION CALL
        uint256 returnValueCall = borrow(e, amount, receiver);

        //VALUES AFTER
        //balances after
        uint256 balanceReceiverAfter = VaultAsset.balanceOf(e, receiver);
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e, currentContract);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e, otherUser);
        BorrowingHarness.VaultCache vaultCacheAfter = CVLUpdateVault();
        //owed after
        BorrowingHarness.Owed owedOnBehalfOfAfter = CVLGetCurrentOwed(onBehalfOf);
        BorrowingHarness.Owed owedOtherUserAfter = CVLGetCurrentOwed(otherUser);
        uint256 userInterestAccumulatorAfter = interestAccumulatorsGhost[onBehalfOf];
        uint256 totalBorrowsAfter = BorrowingHarness.vaultStorage.totalBorrows;

        //ASSERTS
        //assert1: borrow of other user should stay the same
        assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of other user should stay the same");

        //assert2: owed of onBehalfOf account should be increased by the amount borrowed
        assert(to_mathint(owedOnBehalfOfAfter) == owedOnBehalfOfBefore + targetAmountAsOwed, "Owed of onBehalfOf should be increased by the amount borrowed");

        //assert3: cash of the vault should be decreased by the amount borrowed
        assert(cashBefore - targetAmountAsAssets == to_mathint(vaultCacheAfter.cash), "Cash of the vault should be decreased by the amount borrowed");

        //assert4: balance of receiver should be increased by the amount borrowed
        assert(balanceReceiverBefore + targetAmountAsAssets == to_mathint(balanceReceiverAfter), "Balance of the receiver should be increased by the amount borrowed");

        //assert5: balance of vault should be reduced by the amount borrowed
        assert(balanceVaultBefore - targetAmountAsAssets == to_mathint(balanceVaultAfter), "Balance of the vault should be reduced by the amount borrowed");

        //assert6: no other balance should be changed
        assert(balanceOtherUserAfter == balanceOtherUserBefore, "Balance of other user should not be changed");

        //assert7: interestAccumulator of onBehalfOf should be updated
        assert(targetAmountAsAssets != 0 => userInterestAccumulatorAfter == vaultCacheBefore.interestAccumulator, "Interest accumulator should be updated");

        //assert8: total borrows should be increased by the amount borrowed
        assert(totalBorrowsBefore + targetAmountAsOwed == to_mathint(totalBorrowsAfter), "Total borrows should be increased by the amount borrowed");
    }

    //pullDebt reverts  
    rule pullDebtReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address from;
        address onBehalfOf;
        bool vaultIsController;
        onBehalfOf, vaultIsController = EVC.getCurrentOnBehalfOfAccount(e, currentContract);
        BorrowingHarness.VaultCache vaultCache = CVLUpdateVault();
        BorrowingHarness.Owed fromOwedBefore;
        BorrowingHarness.Owed fromPrevOwedBefore;
        fromOwedBefore, fromPrevOwedBefore = loadUserBorrowHarness(vaultCache, from);
        BorrowingHarness.Assets amountAsAssests = amount == max_uint256 ? owedToAssetsUpHarness(e,fromOwedBefore) : unitToAssetsHarness(e, amount);
        BorrowingHarness.Owed amountAsOwed = assetsToOwedHarness(e,amountAsAssests);
        BorrowingHarness.Owed finalAmount = finalAmountDustHarness(amountAsOwed, fromOwedBefore);

        //VALUES BEFORE
        bool isPullDebtDisabled = isPullDebtDisabled(e);

        //FUNCTION CALL
        pullDebt@withrevert(e, amount, from);

        //VALUES AFTER

        //ASSERTS
        //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => lastReverted, "Only EVC can call pullDebt");

        //assert2: if onBehalfOf is 0, then revert
        assert(onBehalfOf == 0 => lastReverted, "On behalf of should not be address(0)");

        //assert3: if vault not controller, then revert
        assert(!vaultIsController => lastReverted, "Vault needs to be controller");

        //assert4: if from = onBehalfOf, then revert
        assert(from == onBehalfOf => lastReverted, "From should not be the same as onBehalfOf");

        //assert5: if finalAmount > fromOwedBefore, then revert
        assert(finalAmount > fromOwedBefore => lastReverted, "Final amount should not be greater than the from owed");

        //assert6: if pullDebt is disabled, then revert
        assert(isPullDebtDisabled => lastReverted, "PullDebt is disabled, functions should revert");
    }

    //pullDebt works
    rule pullDebtIntegraty(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address from;
        address onBehalfOf;
        onBehalfOf = actualCaller(e);
        BorrowingHarness.VaultCache vaultCacheBefore = CVLUpdateVault();
        BorrowingHarness.Assets amountAsAssests = uintToAssetsHarness(e, amount);
        BorrowingHarness.Owed toOwedBefore = CVLGetCurrentOwed(onBehalfOf);
        BorrowingHarness.Owed fromOwedBefore = CVLGetCurrentOwed(from);
        BorrowingHarness.Assets targetAmountAsAssets = 
            amount == max_uint256 ? 
            owedToAssetsUpHarness(e,fromOwedBefore) : 
            amountAsAssests;
        BorrowingHarness.Owed targetAmountAsOwed = assetsToOwedHarness(e,targetAmountAsAssets);
        BorrowingHarness.Owed finalAmountAsOwed = finalAmountDustHarness(e,targetAmountAsOwed, fromOwedBefore);

        //TARGET VALUES
        BorrowingHarness.Owed targetFromOwedAfter = subUncheckedHarness(e, fromOwedBefore, finalAmountAsOwed);
        mathint targetToOwedAfter = toOwedBefore + finalAmountAsOwed;

        //FUNCTION CALL
        uint256 retunrValueCall = pullDebt(e, amount, from);

        //VALUES AFTER
        BorrowingHarness.VaultCache vaultCacheAfter = CVLUpdateVault();
        BorrowingHarness.Owed fromOwedAfter = CVLGetCurrentOwed(from);
        BorrowingHarness.Owed toOwedAfter = CVLGetCurrentOwed(onBehalfOf);
        uint256 toInterestAccumulatorAfter = interestAccumulatorsGhost[onBehalfOf];
        uint256 fromInterestAccumulatorAfter = interestAccumulatorsGhost[from];

        //ASSERTS
        //assert1: owed of from should be decreased by the amount pulled
        assert(targetAmountAsAssets !=0 => targetFromOwedAfter == fromOwedAfter, "Owed should be decreased by the amount pulled");

        //assert2: owed of onBehalfOf should be increased by the amount pulled
        assert(targetAmountAsAssets !=0 => targetToOwedAfter == to_mathint(toOwedAfter), "Owed should be increased by the amount pulled");

        //assert3: interestAccumulator of from should be updated
        assert(targetAmountAsAssets !=0 => fromInterestAccumulatorAfter == vaultCacheBefore.interestAccumulator, "Interest accumulator for from addres should be updated");

        //assert4: interestAccumulator of onBehalfOf should be updated
        assert(targetAmountAsAssets !=0 => toInterestAccumulatorAfter == vaultCacheBefore.interestAccumulator, "Interest accumulator of to address should be updated");

        //assert5: totalBorrowsafter the vault update should stay the same
        assert(vaultCacheBefore.totalBorrows == vaultCacheAfter.totalBorrows, "Total borrows should stay the same");
    }

    //repay reverts
    rule repayReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;

        //VALUES BEFORE
        BorrowingHarness.VaultCache vaultCache = CVLUpdateVault();
        address onBehalfOf = actualCaller(e);
        BorrowingHarness.Owed owed = getCurrentOwedHarness(e,vaultCache, receiver);
        BorrowingHarness.Owed assets = toAssetHarness(amount == max_uint256 ? owed : amount); //i: amount to repay
        bool isRepayDisabled = isRepayDisabled(e);

        //FUNCTION CALL
        repay@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => reverted, "Only EVC can call repay");

        //assert2: if onBehalfOf is address(0), then revert
        assert(onBehalfOf == 0 => reverted, "On behalf of should not be address(0)");

        //assert3: if assets > owed, then revert
        assert(to_mathint(assets) > to_mathint(owed) => reverted, "Amount should not be greater than the owed");

        //assert4: if repay is disabled, then revert
        assert(isRepayDisabled => reverted, "Repay is disabled, functions should revert");
    }

    //repay works
    rule repayIntegraty(env e) {
        //FUNCTION PARAMETER
        address receiver;
        require(receiver != currentContract);
        uint256 amount;
        BorrowingHarness.Assets amountAsAssests = uintToAssetsHarness(e, amount);
        BorrowingHarness.Owed owedReceiverBefore = owedGhost[receiver];
        BorrowingHarness.Assets targetAmountAsAssets = //@audit 
            amount == max_uint256 ? 
            owedToAssetsUpHarness(e, owedReceiverBefore) : 
            amountAsAssests;
        address onBehalfOf = actualCaller(e);
        require(onBehalfOf != currentContract);
        address otherUser;
        require(otherUser != receiver && otherUser != currentContract && otherUser != onBehalfOf);

        //VALUES BEFORE
        BorrowingHarness.Assets owedAssetUp = owedToAssetsUpHarness(e, owedReceiverBefore);
        require(owedAssetUp >= targetAmountAsAssets);
        mathint owedRemainingAsAssetsMathint = owedAssetUp - targetAmountAsAssets;
        require(owedRemainingAsAssetsMathint <= max_uint112);
        BorrowingHarness.Assets owedRemainingAsAssets = assert_uint112(owedRemainingAsAssetsMathint); //@audit casting deos not work
        BorrowingHarness.Owed owedRemainingAsOwed = assetsToOwedHarness(e, owedRemainingAsAssets);

        BorrowingHarness.Assets cashBefore = BorrowingHarness.vaultStorage.cash;
        BorrowingHarness.VaultCache vaultCacheBefore = CVLUpdateVault();
        require(vaultCacheBefore.asset == VaultAsset);
        BorrowingHarness.Owed totalBorrowsBefore = BorrowingHarness.vaultStorage.totalBorrows;
        
        require(to_mathint(totalBorrowsBefore) >= to_mathint(targetAmountAsAssets));
        bool isController = vaultIsController(onBehalfOf);
        mathint targetTotalBorrowsAfter = 
         //i: is the user not the only one that has borrowed
        vaultCacheBefore.totalBorrows > owedReceiverBefore
            ? (totalBorrowsBefore - owedReceiverBefore + owedRemainingAsOwed)
            : owedRemainingAsOwed;

        uint256 userInterestAccumulatorOtherUserBefore = interestAccumulatorsGhost[otherUser];

        //balances before
        uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e, onBehalfOf);
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e, currentContract);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e, otherUser);
        BorrowingHarness.Owed owedOtherUserBefore = owedGhost[otherUser];

        //FUNCTION CALL
        uint256 returnValueCall = repay(e, amount, receiver);

        //VALUES AFTER
        BorrowingHarness.Assets cashAfter = BorrowingHarness.vaultStorage.cash;
        BorrowingHarness.Owed totalBorrowsAfter = BorrowingHarness.vaultStorage.totalBorrows;
        uint256 userInterestAccumulatorReceiverAfter = interestAccumulatorsGhost[receiver];
        uint256 userInterestAccumulatorOtherUserAfter = interestAccumulatorsGhost[otherUser];
        //balances after
        uint256 balanceOnBehalfOfAfter = VaultAsset.balanceOf(e, onBehalfOf);
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e, currentContract);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e, otherUser);
        BorrowingHarness.Owed owedReceiverAfter = owedGhost[receiver];
        BorrowingHarness.Owed owedOtherUserAfter = owedGhost[otherUser];

        //ASSERTS
        //assert0: should pass even if the caller is not the controller (no controller check)//@audit integrate this in an other rule

        //assert1: owed of target account should be decreased by the amount repaid
        assert(targetAmountAsAssets != 0 => owedRemainingAsOwed == owedReceiverAfter, "Owed should be decreased by the amount repaid");

        //assert2: total borrows should be decreased by the amount repaid
        assert(targetAmountAsAssets != 0 => to_mathint(totalBorrowsAfter) == targetTotalBorrowsAfter, "Total borrows should be decreased by the amount repaid");

        //assert3: asset balance of onBehalfOf should be decreased by the amount repaid
        assert(targetAmountAsAssets != 0 => balanceOnBehalfOfBefore - targetAmountAsAssets == to_mathint(balanceOnBehalfOfAfter), "Balance of onBehalfOf should be decreased by the amount repaid");

        //assert4: asset balance of the vault should be increased by the amount repaid
        assert(targetAmountAsAssets != 0 => balanceVaultBefore + targetAmountAsAssets == to_mathint(balanceVaultAfter), "Balance of the vault should be increased by the amount repaid");

        //assert5: no other asset balance should be changed
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should not be changed");

        //assert6: the retunred value should be the amount repaid
        assert(targetAmountAsAssets != 0 => to_mathint(returnValueCall) == to_mathint(targetAmountAsAssets), "Returned value should be the amount repaid");

        //assert7: no other owed should be changed
        assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of other user should not be changed");

        //assert8: userAccumulator od receiver should be updated
        assert(targetAmountAsAssets != 0 => userInterestAccumulatorReceiverAfter == vaultCacheBefore.interestAccumulator, "Interest accumulator should be updated");


        //assert9: cash of the vault should be increased by the amount repaid
        assert(targetAmountAsAssets != 0 => cashBefore + targetAmountAsAssets == to_mathint(cashAfter), "Cash of the vault should be increased by the amount repaid");

        //assert10: the borrow of an other user should stay the same
        assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of other user should stay the same");

        //assert11: userInterestAccumulator of other user should not be changed
        assert(userInterestAccumulatorOtherUserBefore == userInterestAccumulatorOtherUserAfter, "Interest accumulator of other user should not be changed");

    }

    //functions need to revert if reentrancy is locked
    rule reentrancyLockIntegraty(env e, method f, calldataarg args) filtered{f -> NONREENTRANT_FUNCTIONS(f)}{
 
        bool lockedBefore = reentrancyLockedHarness();
        f@withrevert(e, args);

        assert(lockedBefore => lastReverted, "Reentrancy lock did not work");
    }
//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
