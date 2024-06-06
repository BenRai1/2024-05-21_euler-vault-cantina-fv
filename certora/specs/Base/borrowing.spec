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

    //Borrowing functions




    // dispatch and use MockFlashBorrow if more detailed implementation is required
    function _.onFlashLoan(bytes) external => NONDET;

    //Summaries
    function _.resolve(Type.AmountCap self) external => CVLResolve(self) expect (uint256);
    function Cache.updateVault() internal returns (Type.VaultCache memory) with(env e) => CVLUpdateVault();

    //Summary of bowowValues
    //getCurrentOwed(vaultCache, from) from BorrowingUtils 
    //@audit current is previous owed
    function _.getCurrentOwed(Type.VaultCache memory vaultCache, address account) internal => CVLGetCurrentOwed( account) expect (Type.Owed);
    //loadUserBorrow(vaultCache, from) from BorrowingUtils
    function _.loadUserBorrow(Type.VaultCache memory vaultCache, address account) internal => CVLLoadUserBorrow(vaultCache, account) expect (Type.Owed, Type.Owed);
    //setUserBorrow(vaultCache, to, toOwed) from BorrowingUtils
    function _.setUserBorrow(Type.VaultCache memory vaultCache, address account, Type.Owed newOwed) internal => CVLSetUserBorrow(vaultCache, account, newOwed) expect void;

    //Summary of share values
    function _.getBalanceAndBalanceForwarder(Type.PackedUserSlot data, uint256 interestAccumulator) internal => 
    CVLGetBalanceAndBalanceForwarder(data) expect (Type.Shares, bool);

    function _.getBalance(Type.PackedUserSlot data, uint256 interestAccumulator) internal => CVLGetBalance(data) expect (Type.Shares);

    function _.setBalance(Type.PackedUserSlot data, Type.Shares balance) internal => CVLSetBalance(data, balance) expect void;


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
    function CVLUpdateVault() returns Type.VaultCache {
            Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }

    function CVLGetCurrentOwed(address account) returns Type.Owed {
        return owedGhost[account];

    }

    function CVLLoadUserBorrow(Type.VaultCache vaultCache, address account) returns (Type.Owed, Type.Owed){
        return (owedGhost[account], owedGhost[account]);
    }

    function CVLSetUserBorrow(Type.VaultCache vaultCache, address account, Type.Owed newOwed){
        owedGhost[account] = newOwed;
        interestAccumulatorsGhost[account] = vaultCache.interestAccumulator;
    }

    //-----------------SHARES / BALANCES-----------------
    function CVLGetBalanceAndBalanceForwarder(Type.PackedUserSlot data) returns (Type.Shares, bool){
        address onBehalfOf = storageToUserGhost[data];
        return (sharesGhost[onBehalfOf], balanceForwarderEnabledGhost[onBehalfOf]);
    }

    function CVLGetBalance(Type.PackedUserSlot userStorageData) returns Type.Shares{
        return sharesGhost[storageToUserGhost[userStorageData]];
    }

    function CVLSetBalance(Type.PackedUserSlot userStorageData, Type.Shares balance){
        sharesGhost[storageToUserGhost[userStorageData]] = balance; //i: set the ghost shares
    }  

    //ghost shares
    //each user has a unique userStorage => mapping userstorage to user
    ghost mapping(Type.PackedUserSlot => address) storageToUserGhost;
        
    //user is used to look up the shares in the ghost mapping sharesGhost
    ghost mapping(address => Type.Shares) sharesGhost;

    //ghost balanceForwarderEnabled
    ghost mapping(address => bool) balanceForwarderEnabledGhost;



////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

//ghost borrows
ghost mapping(address => Type.Owed) owedGhost;
ghost mapping(address =>  uint256) interestAccumulatorsGhost;




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
