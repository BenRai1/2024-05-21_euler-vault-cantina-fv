import "../Base.spec";
import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
methods {
    function isRecognizedCollateralExt(address collateral) external returns (bool) envfree;
    function getCurrentVaultCacheHarness() external returns (LiquidationHarness.VaultCache memory) envfree;

    //Function summaries
    function Cache.loadVault() internal returns (LiquidationHarness.VaultCache memory) with(env e) => CVLLoadVault();
    function Cache.updateVault() internal returns (LiquidationHarness.VaultCache memory) with(env e) => CVLUpdateVault();
}

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////
    function CVLLoadVault() returns LiquidationHarness.VaultCache {
            LiquidationHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }

    function CVLUpdateVault() returns LiquidationHarness.VaultCache {
            LiquidationHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }


////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
