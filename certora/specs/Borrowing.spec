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




//repay works
rule repayIntegraty(env e) {
    //FUNCTION PARAMETER
    uint256 amount;
    address receiver;
    address onBehalfOf = actualCaller(e);
    require(onBehalfOf != currentContract);
    address otherUser;
    require(otherUser != receiver && otherUser != currentContract && otherUser != onBehalfOf);

    //VALUES BEFORE
    BorrowingHarness.Assets cashBefore = BorrowingHarness.vaultStorage.cash;
    BorrowingHarness.Owed totalBorrowsBefore = getTotalBorrowsHarness();
    BorrowingHarness.VaultCache vaultCache = CVLUpdateVault();
    require(vaultCache.asset == VaultAsset);
    
    uint256 owedBefore = toAssetsUpHarness(e, getCurrentOwedHarness(vaultCache, receiver));
    // BorrowingHarness.Assets owedBeforeUp = toAssetsUpHarness(owedBefore);
    BorrowingHarness.Owed owedOtherUserBefore = getCurrentOwedHarness(vaultCache, otherUser);
    BorrowingHarness.Assets assetsRepayed = toAssetHarness(amount == max_uint256 ? owedBefore : amount); //i: amount to repay
    require(to_mathint(totalBorrowsBefore) >= to_mathint(assetsRepayed));
    bool isController = vaultIsController(onBehalfOf);
    //balances before
    uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e, onBehalfOf);
    uint256 balanceVaultBefore = VaultAsset.balanceOf(e, currentContract);
    uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e, otherUser);

    //FUNCTION CALL
    uint256 returnValueCall = repay(e, amount, receiver);

    //VALUES AFTER
    BorrowingHarness.Assets cashAfter = BorrowingHarness.vaultStorage.cash;
    BorrowingHarness.Owed totalBorrowsAfter = getTotalBorrowsHarness();
    BorrowingHarness.Owed owedAfter = getCurrentOwedHarness(vaultCache, receiver);
    BorrowingHarness.Owed owedOtherUserAfter = getCurrentOwedHarness(vaultCache, otherUser);
    uint256 userInterestAccumulatorAfter = getUserInterestAccumulatorHarness(receiver);
    //balances after
    uint256 balanceOnBehalfOfAfter = VaultAsset.balanceOf(e, onBehalfOf);
    uint256 balanceVaultAfter = VaultAsset.balanceOf(e, currentContract);
    uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e, otherUser);



    //ASSERTS
    //assert0: should pass even if the caller is not the controller (no controller check)//@audit integrate this in an other rule


    //assert1: owed of target account should be decreased by the amount repaid
    assert(assetsRepayed != 0 => owedBefore - assetToOwedHarness(e, assetsRepayed) == to_mathint(toAssetsUpHarness(e,owedAfter)), "Owed should be decreased by the amount repaid");

    // //assert2: total borrows should be decreased by the amount repaid//@audit assetsRepayed must be transformed into Borrow
    // assert(assetsRepayed != 0 => totalBorrowsBefore - assetToOwedHarness(e,assetsRepayed) == to_mathint(totalBorrowsAfter), "Total borrows should be decreased by the amount repaid");



    



    ///----------------------ASSERTS OK START-------------------------
        // //assert3: asset balance of onBehalfOf should be decreased by the amount repaid
        // assert(assetsRepayed != 0 => balanceOnBehalfOfBefore - assetsRepayed == to_mathint(balanceOnBehalfOfAfter), "Balance of onBehalfOf should be decreased by the amount repaid");


        // //assert4: asset balance of the vault should be increased by the amount repaid
        // assert(assetsRepayed != 0 => balanceVaultBefore + assetsRepayed == to_mathint(balanceVaultAfter), "Balance of the vault should be increased by the amount repaid");

        // //assert5: no other asset balance should be changed
        // assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should not be changed");

        // //assert6: the retunred value should be the amount repaid
        // assert(assetsRepayed != 0 => to_mathint(returnValueCall) == to_mathint(assetsRepayed), "Returned value should be the amount repaid");

        // //assert7: no other owed should be changed
        // assert(owedOtherUserBefore == owedOtherUserAfter, "Owed of other user should not be changed");

        // //assert8: userAccumulator should be updated
        // assert(assetsRepayed != 0 => userInterestAccumulatorAfter == vaultCache.interestAccumulator, "Interest accumulator should be updated");


        // //assert9: cash of the vault should be increased by the amount repaid
        // assert(assetsRepayed != 0 => cashBefore + assetsRepayed == to_mathint(cashAfter), "Cash of the vault should be increased by the amount repaid");

    ///----------------------ASSERTS OK END-------------------------
}








//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------
    //borrow pass work
    rule borrowIntegratyPass(env e) {
        uint256 amount;//used
        BorrowingHarness.Assets assets = toAssetHarness(amount);//used
        BorrowingHarness.Owed owed = toOwedHarness(assets); //used
        address receiver; //used
        BorrowingHarness.VaultCache vaultCache;
        address onBehalfOf;
        uint32 operation = OP_BORROW_Harness();
        address accountToCheck = CHECKACCOUNT_CALLER_Harness();
        storage initial = lastStorage;
        (vaultCache, onBehalfOf) = initOperationExternal@withrevert(e, operation, accountToCheck); //withrevert to be able to check for reverts later



        //values before
        BorrowingHarness.Owed totalBorrowsBefore = getTotalBorrowsHarness();
        // //userStorage of onBehalfOf
        // BorrowingHarness.Owed owedBefore = getUserBorrowHarness(e, vaultCache.interestAccumulator, onBehalfOf);


        //function call
        uint256 result = borrow(e, amount, receiver) at initial;
        
        
        //values after
        uint256 totalBorrowsAfter = getTotalBorrowsHarness();
        // //userStorage of onBehalfOf
        // BorrowingHarness.Owed owedAfter = getUserBorrowHarness(e, vaultCache.interestAccumulator, onBehalfOf);
        uint256 userInterestAccumulatorAfter = getUserInterestAccumulatorHarness(onBehalfOf);

        //asserts

       

        // //assert4: userStorageAfter.interestAccumulator == vaultCache.interestAccumulator
        // assert(userInterestAccumulatorAfter == vaultCache.interestAccumulator, "Interest accumulator should be the same");



        //----------------------ASSERTS TESTED START-------------------------
        //assert1: total borrowBefore + owed == totalBorrowsAfter
        assert(totalBorrowsBefore + owed == to_mathint(totalBorrowsAfter), "Total borrows should be increased by the amount borrowed");

        // //assert2: if the amount is 0 or amount is type(uint256).max and cash is 0 return 0
        // assert(amount == 0 || (amount == max_uint256 && vaultCache.cash == 0) => result == 0, "Amount should not be 0");

         // //assert3: owedAfter == owedBefore + owed
        // assert(to_mathint(owedAfter) == owedBefore + owed, "Owed should be increased by the amount borrowed");
        //----------------------ASSERTS TESTED END-------------------------

        //----------------------ASSERTS OK START-------------------------

        //----------------------ASSERTS OK END-------------------------

    }

       

    //borrow Reverts work
    rule borrowIntegratyReverts(env e) {
        uint256 amount;
        BorrowingHarness.Assets assets = toAssetHarness(amount);
        address receiver;
        uint32 operation = OP_BORROW_Harness();
        address accountToCheck = CHECKACCOUNT_CALLER_Harness();
        BorrowingHarness.VaultCache vaultCache;
        address onBehalfOf;
        storage initial = lastStorage;
        (vaultCache, onBehalfOf) = initOperationExternal@withrevert(e, operation, accountToCheck); //withrevert to be able to check for reverts later

        //controller
        bool vaultIsController = vaultIsController(currentContract);

        //function call
        borrow@withrevert(e, amount, receiver) at initial;
        bool reverted = lastReverted;

       
    


     

     /// --------------------- ASSERTS Tested Start -------------------------

        // //controller should be checked => if currentContract not controller, then revert
        // assert(!vaultIsController => reverted, "Vault needs to be controller");


        //assert4: if assets > vaultCache.cash, then revert
        assert(assets > vaultCache.cash => reverted, "Amount should not be greater than the vault cash");

     /// --------------------- ASSERTS Tested End -------------------------
    
     ///--------------------Asserts OK START -------------------------

        // //revert if msg.sender is not evc
        // assert(evcHarness() != e.msg.sender => reverted, "Only EVC can call borrow");

     ///--------------------Asserts OK END -------------------------
    }

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

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
    }

    //functions need to revert if reentrancy is locked
    rule reentrancyLockIntegraty(env e, method f, calldataarg args) filtered{f -> nonReentrantFunctions(f)}{
 
        bool lockedBefore = reentrancyLockedHarness();
        f@withrevert(e, args);

        assert(lockedBefore => lastReverted, "Reentrancy lock did not work");
    }
//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
