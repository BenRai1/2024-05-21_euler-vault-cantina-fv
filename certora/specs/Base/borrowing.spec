import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
methods {
    //Harness functions
    function reentrancyLockedHarness() external returns (bool) envfree;
    function OP_BORROW_Harness() external returns (uint32) envfree;
    function CHECKACCOUNT_CALLER_Harness() external returns (address) envfree;
    function evcHarness() external returns (address) envfree;
    function toAssetHarness(uint256 amount) external returns (BorrowingHarness.Assets) envfree;
    function toOwedHarness(BorrowingHarness.Assets self) external returns (BorrowingHarness.Owed) envfree;
    function getTotalBorrowsHarness() external returns (BorrowingHarness.Owed) envfree;	
    // function getNewOwedHarness(BorrowingHarness.UserStorage memory self, BorrowingHarness.Owed owed) external returns (BorrowingHarness.PackedUserSlot) envfree;
    function getUserInterestAccumulatorHarness(address account) external returns (uint256) envfree;
    function getCurrentVaultCacheHarness() external returns (BorrowingHarness.VaultCache memory) envfree;
    function getCurrentOwedHarness(BorrowingHarness.VaultCache vaultCache, address account) external returns (BorrowingHarness.Owed) envfree;
    function loadUserBorrowHarness(BorrowingHarness.VaultCache vaultCache, address account) external returns (BorrowingHarness.Owed, BorrowingHarness.Owed) envfree;



    // dispatch and use MockFlashBorrow if more detailed implementation is required
    function _.onFlashLoan(bytes) external => NONDET;

    //Summaries
    function _.resolve(BorrowingHarness.AmountCap self) external => CVLResolve(self) expect (uint256);
    function Cache.updateVault() internal returns (BorrowingHarness.VaultCache memory) with(env e) => CVLUpdateVault();

    //Summary of bowowValues
    //getCurrentOwed(vaultCache, from) from BorrowingUtils 
    //@audit current is previous owed
    function _.getCurrentOwed(BorrowingHarness.VaultCache memory vaultCache, address account) internal => CVLGetCurrentOwed( account) expect (BorrowingHarness.Owed);
    //loadUserBorrow(vaultCache, from) from BorrowingUtils
    function _.loadUserBorrow(BorrowingHarness.VaultCache memory vaultCache, address account) internal => CVLLoadUserBorrow(vaultCache, account) expect (BorrowingHarness.Owed, BorrowingHarness.Owed);
    //setUserBorrow(vaultCache, to, toOwed) from BorrowingUtils
    function _.setUserBorrow(BorrowingHarness.VaultCache memory vaultCache, address account, BorrowingHarness.Owed newOwed) internal => CVLSetUserBorrow(vaultCache, account, newOwed) expect void;


}


/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

    definition nonReentrantFunctions(method f) returns bool =
    f.selector == sig:borrow(uint256, address).selector ||
    f.selector == sig:flashLoan(uint256, bytes).selector ||
    f.selector == sig:pullDebt(uint256, address).selector ||
    f.selector == sig:repay(uint256, address).selector ||
    f.selector == sig:repayWithShares(uint256, address).selector ||
    f.selector == sig:touch().selector;





///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////
    function CVLUpdateVault() returns BorrowingHarness.VaultCache {
            BorrowingHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }

    function CVLGetCurrentOwed(address account) returns BorrowingHarness.Owed {
        return owedGhost[account];

    }

    function CVLLoadUserBorrow(BorrowingHarness.VaultCache vaultCache, address account) returns (BorrowingHarness.Owed, BorrowingHarness.Owed){
        return (owedGhost[account], owedGhost[account]);
    }

    function CVLSetUserBorrow(BorrowingHarness.VaultCache vaultCache, address account, BorrowingHarness.Owed newOwed){
        owedGhost[account] = newOwed;
        interestAccumulatorsGhost[account] = vaultCache.interestAccumulator;
    }

////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

//ghost borrows
ghost mapping(address => BorrowingHarness.Owed) owedGhost;
ghost mapping(address =>  uint256) interestAccumulatorsGhost;


//ghost Caps

ghost BorrowingHarness.AmountCap supplyCapGhost;

hook Sload BorrowingHarness.AmountCap returnValue currentContract.vaultStorage.supplyCap{
    require(supplyCapGhost == returnValue);
} 


//wenn vaultStorage.supplyCap is red, make sure it returns supplyCapGhost

ghost BorrowingHarness.AmountCap borrowCapGhost; 

hook Sload BorrowingHarness.AmountCap returnValue currentContract.vaultStorage.borrowCap{
    require(borrowCapGhost == returnValue);
} 

function CVLResolve(BorrowingHarness.AmountCap self) returns uint256{
    return assert_uint256(self / 64 * 10^63); 
}



///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
