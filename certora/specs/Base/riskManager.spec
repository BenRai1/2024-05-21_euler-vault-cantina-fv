import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
     methods {
        //Harness functions
        function getOwedHarness(address account) external returns(RiskManagerHarness.Owed) envfree;
        function getCurrentVaultCacheHarness() external returns (RiskManagerHarness.VaultCache memory) envfree;
        function getSnapshotHarness() external returns (RiskManagerHarness.Snapshot) envfree;
        function toAssetUPHarness(RiskManagerHarness.Owed amount) external returns (RiskManagerHarness.Assets) envfree;
        function toUintHarness(RiskManagerHarness.Assets amount) external returns (uint256) envfree;
        function totalAssetsHarness(RiskManagerHarness.VaultCache vaultCache) external returns (uint256) envfree;


        //Function summaries    
        function Cache.updateVault() internal returns (RiskManagerHarness.VaultCache memory) with(env e) => CVLUpdateVault();
        function Cache.loadVault() internal returns (RiskManagerHarness.VaultCache memory) with(env e) => CVLLoadVault();

        function _.useViewCaller() internal => CVLUseViewCaller() expect address;

     }

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////
  definition HARNESSES_FUNCTIONS(method f) returns bool =
        f.selector == sig:getOwedHarness(address).selector ||
        f.selector == sig:getCurrentVaultCacheHarness().selector ||
        f.selector == sig:getSnapshotHarness().selector ||
        f.selector == sig:toAssetUPHarness(RiskManagerHarness.Owed).selector ||
        f.selector == sig:toUintHarness(RiskManagerHarness.Assets).selector ||
        f.selector == sig:getCollateralValueHarness(RiskManagerHarness.VaultCache,address,address[],bool).selector ||
        f.selector == sig:getCollateralValuesHarness(RiskManagerHarness.VaultCache,address,address[],bool).selector ||
        f.selector == sig:getLiabilityValueHarness(RiskManagerHarness.VaultCache,address,RiskManagerHarness.Owed,bool).selector ||
        f.selector == sig:totalAssetsHarness(RiskManagerHarness.VaultCache).selector;

///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////

        function CVLUpdateVault() returns RiskManagerHarness.VaultCache {
                RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
                return vaultCache;
        }

        function CVLLoadVault() returns RiskManagerHarness.VaultCache {
                RiskManagerHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
                return vaultCache;
        }

        function CVLUseViewCaller() returns address {
                return viewCallerGhost;
        }

        ghost address viewCallerGhost;





////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
