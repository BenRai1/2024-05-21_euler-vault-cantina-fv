import "../Base.spec";
import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
methods {
    function isRecognizedCollateralExt(address collateral) external returns (bool) envfree;
    function getCurrentVaultCacheHarness() external returns (Type.VaultCache memory) envfree;
    function checkNoCollateralHarness(address account, address[] collaterals) external returns (bool) envfree;
    function socializeDebtHarness(Type.Flags configFlags) external returns(bool) envfree;

    //Function summaries
    function Cache.loadVault() internal returns (Type.VaultCache memory) with(env e) => CVLLoadVault();
    function Cache.updateVault() internal returns (Type.VaultCache memory) with(env e) => CVLUpdateVault();

    //Summary of bowowValues
    //@audit current is previous owed
    function _.getCurrentOwed(Type.VaultCache memory vaultCache, address account) internal => CVLGetCurrentOwed( account) expect (Type.Owed);
    //loadUserBorrow(vaultCache, from) from BorrowingUtils
    function _.loadUserBorrow(Type.VaultCache memory vaultCache, address account) internal => CVLLoadUserBorrow(vaultCache, account) expect (Type.Owed, Type.Owed);
    //setUserBorrow(vaultCache, to, toOwed) from BorrowingUtils
    function _.setUserBorrow(Type.VaultCache memory vaultCache, address account, Type.Owed newOwed) internal => CVLSetUserBorrow(vaultCache, account, newOwed) expect void;

    function _.enforceCollateralTransfer(address collateral, uint256 amount, address from, address receiver) internal => CVLEnforceCollateralTransfer(collateral, amount, from, receiver) expect void;

    function DummyERC20A.balanceOf(address account) external returns (uint256) => CVLBalanceOfCollateral(account);


}

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////
    function CVLLoadVault() returns Type.VaultCache {
            Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }

    function CVLUpdateVault() returns Type.VaultCache {
            Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }


    //---------------------- Summary of borowValues ----------------------
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

    //ghost borrows
    ghost mapping(address => Type.Owed) owedGhost;
    ghost mapping(address =>  uint256) interestAccumulatorsGhost;

    //---------------------- Summary of collateral balances and enforceCollateralTransfer ----------------------

    function CVLEnforceCollateralTransfer(address collateral, uint256 amount, address from, address receiver){
        collateralBalancesGhost[from] = require_uint256(collateralBalancesGhost[from] - amount);
        collateralBalancesGhost[receiver] = require_uint256(collateralBalancesGhost[receiver] + amount);

    }

    function CVLBalanceOfCollateral(address account) returns uint256 {
        return collateralBalancesGhost[account];
    }

    ghost mapping(address => uint256) collateralBalancesGhost;




////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
