import "../Base/abstractBase.spec";


// used to test running time
use builtin rule sanity;

methods{
     function getUserInterestAccumulatorHarness(address account) external returns(uint256) envfree;
     function getGlobalInterestAccumulatorHarness() external returns(uint256) envfree;
}
//@audit add "otherUser" to BalanceUtils

//------------------------------- RULES TEST START ----------------------------------


//invariants:


// //invarient totalBorrowed is the sum of all borrows
// invariant totalBorrowsSumOfUserBorrowsInvariant(address alice, address bob, address charlie, env e)
//     (alice != bob && alice != charlie && bob != charlie) => //@audit-issue currentUserBorrowHarness needs a vaultCache => should be fine to only use the normal borrow since the data was updates => need to ensure that vaultCache.interestAccumulator == user interestAccumulator
//     to_mathint(getTotalBorrowsHarness(e)) == currentUserBorrowHarness(alice) + currentUserBorrowHarness(bob) + currentUserBorrowHarness(charlie)
//     filtered{
//         f-> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)
//     }
//     {
//         preserved transferBorrowHarness(Type.VaultCache vaultCache, address from, address to, Type.Assets assets) {
//             require(from == alice || from == bob || from == charlie);
//             require(to == alice || to == bob || to == charlie);
//         }

//         preserved increaseBorrowHarness(Type.VaultCache vaultCache, address account, Type.Assets assets) {
//             require(account == alice || account == bob || account == charlie);
//         }

//         preserved decreaseBorrowHarness(Type.VaultCache vaultCache, address account, Type.Assets assets) {
//             require(account == alice || account == bob || account == charlie);
//         }

// }


//increaseBorrow works
rule increaseBorrowWorks(env e){
    //FUNCTION PARAMETERS
    Type.VaultCache vaultCache;
    require(vaultCache.interestAccumulator == getGlobalInterestAccumulatorHarness());
    address account;
    requireInvariant interestAccumulatorInvariant(account);
    Type.Assets asset;
    Type.Owed assetAsOwed = assetsToOwedHarness(asset);
    address otherUser;
    require(account != otherUser);

    //VALUES BEFORE
    Type.Owed totalBorrowedBefore = getTotalBorrowsHarness(e);
    require(totalBorrowedBefore == vaultCache.totalBorrows);
    Type.Owed accountBorrowedBefore = currentUserBorrowHarness(e, vaultCache, account);
    Type.Owed otherUserBorrowedBefore = currentUserBorrowHarness(e, vaultCache, otherUser);

    //CALL FUNCTION
    increaseBorrowHarness(e, vaultCache, account, asset);

    //VALUES AFTER
    Type.Owed totalBorrowedAfter = getTotalBorrowsHarness(e);
    Type.Owed accountBorrowedAfter = currentUserBorrowHarness(e, vaultCache, account);
    Type.Owed otherUserBorrowedAfter = currentUserBorrowHarness(e, vaultCache, otherUser);
    uint256 interestAccumulatorAccountAfter = getUserInterestAccumulatorHarness(account);


    //ASSERTS
    //assert1: totalBorrowed increases by the amount borrowed
    assert(to_mathint(totalBorrowedAfter) == totalBorrowedBefore + assetAsOwed, "totalBorrowed did not increase by the amount borrowed");

    //assert2: accountBorrowed increases by the amount borrowed
    assert(to_mathint(accountBorrowedAfter) == accountBorrowedBefore + assetAsOwed, "accountBorrowed did not increase by the amount borrowed");

    //assert3: otherUserBorrowed stays the same
    assert(otherUserBorrowedAfter == otherUserBorrowedBefore, "otherUserBorrowed changed");

    //assert4: interestAccumulator account is the same as vaultCacheBefore.interestAccumulator
    assert(interestAccumulatorAccountAfter == vaultCache.interestAccumulator, "interestAccumulator of account changed");  

}

//decreaseBorrow works
rule decreaseBorrowWorks(env e){
    //FUNCTION PARAMETERS
    Type.VaultCache vaultCache;
    require(vaultCache.interestAccumulator == getGlobalInterestAccumulatorHarness());
    address account;
    requireInvariant interestAccumulatorInvariant(account);
    Type.Assets asset;
    Type.Owed assetAsOwed = assetsToOwedHarness(asset);
    address otherUser;
    require(account != otherUser);

    //VALUES BEFORE
    Type.Owed totalBorrowedBefore = getTotalBorrowsHarness(e);
    require(totalBorrowedBefore == vaultCache.totalBorrows);
    Type.Owed accountBorrowedBefore = currentUserBorrowHarness(e, vaultCache, account);
    require(accountBorrowedBefore <= totalBorrowedBefore); //@audit make this an invariant
    Type.Owed otherUserBorrowedBefore = currentUserBorrowHarness(e, vaultCache, otherUser);
    //targetValues
    mathint targetTotalBorrowed = vaultCache.totalBorrows > accountBorrowedBefore
            ? vaultCache.totalBorrows - assetAsOwed
            : accountBorrowedBefore-assetAsOwed;


    //CALL FUNCTION
    decreaseBorrowHarness@withrevert(e, vaultCache, account, asset);
    bool reverted = lastReverted;

    //VALUES AFTER
    Type.Owed totalBorrowedAfter = getTotalBorrowsHarness(e);
    Type.Owed accountBorrowedAfter = currentUserBorrowHarness(e, vaultCache, account);
    Type.Owed otherUserBorrowedAfter = currentUserBorrowHarness(e, vaultCache, otherUser);
    uint256 interestAccumulatorAccountAfter = getUserInterestAccumulatorHarness(account);

    //ASSERTS
    //assert1: totalBorrowed decreases by the amount borrowed
    assert(!reverted => to_mathint(totalBorrowedAfter) == targetTotalBorrowed, "totalBorrowed did not decrease by the amount borrowed");

    //assert2: accountBorrowed decreases by the amount borrowed
    assert(!reverted => to_mathint(accountBorrowedAfter) == accountBorrowedBefore - assetAsOwed, "accountBorrowed did not decrease by the amount borrowed");

    //assert3: otherUserBorrowed stays the same
    assert(!reverted => otherUserBorrowedAfter == otherUserBorrowedBefore, "otherUserBorrowed changed");

    //assert4: if accountBorrowedBefore < assetAsOwed, function should revert
    assert(assetAsOwed > accountBorrowedBefore => reverted, "function did not revert when assetAsOwed > accountBorrowedBefore");

    //assert5: interestAccumulatorUserAfter is the same as vaultCacheBefore.interestAccumulator 
    assert(interestAccumulatorAccountAfter == vaultCache.interestAccumulator, "interestAccumulator of account changed");

}





//transferBorrow works
//computeInterestRate works
//getCurrentOwed works
//onlyIncreasesUserBorrow
//onlyDecreasesUserBorrow
//onlyIncreasesTotalBorrow
//onlyDecreasesTotalBorrow
//onlyChangesInterestRate


//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------
    //invariant: InterestAccumulator of user is <= interestAccumulator of VaultStorage
    invariant interestAccumulatorInvariant(address user)
        getUserInterestAccumulatorHarness(user) <= getGlobalInterestAccumulatorHarness()
        filtered{
            f-> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)
        }
        {
            preserved increaseBorrowHarness(Type.VaultCache vaultCache, address account, Type.Assets assets) with (env e){
                require(vaultCache.interestAccumulator == getGlobalInterestAccumulatorHarness());
            }

            preserved decreaseBorrowHarness(Type.VaultCache vaultCache, address account, Type.Assets assets) with (env e){
                require(vaultCache.interestAccumulator == getGlobalInterestAccumulatorHarness());
            }

            preserved transferBorrowHarness(Type.VaultCache vaultCache, address from, address to, Type.Assets assets) with (env e){
                require(vaultCache.interestAccumulator == getGlobalInterestAccumulatorHarness());
            }
    }

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
