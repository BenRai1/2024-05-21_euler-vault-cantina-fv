import "./Base.spec";
import "./Base/borrowing.spec";



// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

//invariants: 
//- interestAccumulator of a user account is never bigger than the global interestAccumulator

//------------------------------- RULES TEST START ----------------------------------









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
