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



    // dispatch and use MockFlashBorrow if more detailed implementation is required
    function _.onFlashLoan(bytes) external => NONDET;

    //Summaries
    function _.resolve(BorrowingHarness.AmountCap self) external => CVLResolve(self) expect (uint256);
    function Cache.updateVault() internal returns (BorrowingHarness.VaultCache memory) with(env e) => CVLUpdateVault();

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

////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

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
