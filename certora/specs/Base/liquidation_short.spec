import "../Base.spec";
import "./abstractBase.spec";
/////////////////// METHODS START ///////////////////////
methods {
    function isRecognizedCollateralExt(address collateral) external returns (bool) envfree;
    function getCurrentVaultCacheHarness() external returns (LiquidationHarness.VaultCache memory) envfree;

    //Function summaries
    function Cache.loadVault() internal returns (LiquidationHarness.VaultCache memory) with(env e) => CVLLoadVault();
    //@audit summarize the private function to go to a CVL function which does the same => Call the CVL function to get the results so it can be checked
}

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////
    function CVLLoadVault() returns LiquidationHarness.VaultCache {
            LiquidationHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }


////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
