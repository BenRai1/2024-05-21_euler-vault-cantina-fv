import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
methods {
    //Harness functions
    function reentrancyLockedHarness() external returns (bool) envfree;
    function OP_BORROW_Harness() external returns (uint32) envfree;
    function CHECKACCOUNT_CALLER_Harness() external returns (address) envfree;
    function evcHarness() external returns (address) envfree;
    function toAssetHarness(uint256 amount) external returns (Type.Assets) envfree;
    function toOwedHarness(Type.Assets self) external returns (Type.Owed) envfree;
    function getTotalBorrowsHarness() external returns (Type.Owed) envfree;	
    // function getNewOwedHarness(Type.UserStorage memory self, Type.Owed owed) external returns (Type.PackedUserSlot) envfree;
    function getUserInterestAccumulatorHarness(address account) external returns (uint256) envfree;
    function getCurrentVaultCacheHarness() external returns (Type.VaultCache memory) envfree;
    function getCurrentOwedHarness(Type.VaultCache vaultCache, address account) external returns (Type.Owed) envfree;
    function loadUserBorrowHarness(Type.VaultCache vaultCache, address account) external returns (Type.Owed, Type.Owed) envfree;
    function finalAmountDustHarness(Type.Owed amount, Type.Owed currentOwed) external returns (Type.Owed) envfree;
    function getUserCollateralBalanceHarness(Type.VaultCache vaultcache, address user) external returns (uint256) envfree;

    //Borrowing functions




    // dispatch and use MockFlashBorrow if more detailed implementation is required
    function _.onFlashLoan(bytes) external => NONDET;

    //Summaries
    function _.resolve(Type.AmountCap self) external => CVLResolve(self) expect (uint256);
    function Cache.updateVault() internal returns (Type.VaultCache memory) with(env e) => CVLUpdateVault();

    // function _.initOperation(uint32 operation, address accountToCheck) 
    //     internal with (env e) => CVLInitOperation(e) expect (Type.VaultCache memory, address); //@audit-issue should be removed for the "revert" rules

    // function _.getBalance(Type.UserStorage storage self) internal => CVLGetBalance(self.data) expect (Type.Shares);



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

    definition BORROWING_HARNESS_FUNCTIONS(method f) returns bool =
    f.selector == sig:getBalanceAndForwarderExt(address).selector ||
    f.selector == sig:getCurrentVaultCacheHarness().selector ||
    f.selector == sig:getUnderlyingAssetExt().selector ||
    f.selector == sig:getVaultInterestAccExt().selector ||
    f.selector == sig:initOperationExternal(uint32,address).selector ||
    f.selector == sig:loadUserBorrowHarness(Type.VaultCache,address).selector ||
    f.selector == sig:repayWithSharesCalculationHarness(uint256,Type.Shares,Type.VaultCache,Type.Assets).selector;
    






///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////
    // function CVLGetBalance(Type.PackedUserSlot self) returns Type.Shares {
    //     return sharesGhost;
    // }

    // ghost Type.Shares sharesGhost;

    // ghost mapping(Type.PackedUserSlot => Type.Shares) userSharesGhost;

    // function CVLInitOperation(env e) returns (Type.VaultCache, address) {
    //     Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
    //     address account = actualCaller(e);
    //     return (vaultCache, account);
    // }

    function CVLUpdateVault() returns Type.VaultCache {
            Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }


    //-----------------SHARES / BALANCES-----------------
   

   
    


////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

//ghost borrows


//ghost Caps

ghost Type.AmountCap supplyCapGhost;

hook Sload Type.AmountCap returnValue currentContract.vaultStorage.supplyCap{
    require(supplyCapGhost == returnValue);
} 


//wenn vaultStorage.supplyCap is red, make sure it returns supplyCapGhost

ghost Type.AmountCap borrowCapGhost; 

hook Sload Type.AmountCap returnValue currentContract.vaultStorage.borrowCap{
    require(borrowCapGhost == returnValue);
} 

function CVLResolve(Type.AmountCap self) returns uint256{
    return assert_uint256(self / 64 * 10^63); 
}





///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
