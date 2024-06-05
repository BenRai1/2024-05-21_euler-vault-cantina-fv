
/////////////////// METHODS START ///////////////////////
methods {
    //Harness functions
    function getHookTargetHarness() external returns (address) envfree;
    function useViewCallerHarness() external returns (address) envfree;
    function reentrancyLockedHarness() external returns (bool) envfree;
    function getControlersExt(address account) external returns (address[] memory) envfree;
    function _.uintToAssetsUpHarness(uint256 amount) external envfree;
    function _.assetToOwedHarness(Type.Assets self) external envfree;
    function owedToAssetsUpHarness(Type.Owed amount) external returns (Type.Assets) envfree;
    function isNotSetCompatibeAssetHarness(Type.Flags self) external returns (bool) envfree;
    function isKnownNonOwnerAccountHarness(address account) external returns (bool) envfree;
    function uintToAssetsHarness(uint256 amount) external returns (Type.Assets) envfree;
    function uintToAssetsUpHarness(uint256 amount) external returns (Type.Assets) envfree;
    function unitToAssetsHarness(uint256 amount) external returns (Type.Assets) envfree;
    function owedToAssetsUpHarness(Type.Owed amount) external returns (Type.Assets) envfree;
    function sharesToAssetsDownHarness(Type.Shares amount, Type.VaultCache vaultCache) external returns (Type.Assets) envfree;
    function assetToOwedHarness(Type.Assets self) external returns (Type.Owed) envfree;
    function uintToOwedHarness(uint256 amount) external returns (Type.Owed) envfree;
    function subUncheckedHarness(Type.Owed a, Type.Owed b) external returns (Type.Owed) envfree;
    function addUncheckedHarness(Type.Owed a, Type.Owed b) external returns (Type.Owed) envfree;
    function assetsToSharesUpHarness(Type.Assets self, Type.VaultCache vaultCache) external returns (Type.Shares) envfree;


    function _.balanceOf(address account) external envfree;

}

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

definition BASE_HARNESS_FUNCTIONS(method f) returns bool =
    f.selector == sig:getHookTargetHarness().selector ||
    f.selector == sig:useViewCallerHarness().selector ||
    f.selector == sig:isDepositDisabled().selector ||
    f.selector == sig:isMintDisabled().selector ||
    f.selector == sig:isOperationDisabledExt(uint32).selector ||
    f.selector == sig:isRedeemDisabled().selector ||
    f.selector == sig:isSkimDisabled().selector ||
    f.selector == sig:isWithdrawDisabled().selector ||
    f.selector == sig:vaultCacheOracleConfigured().selector ||
    f.selector == sig:reentrancyLockedHarness().selector;

///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////

////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
