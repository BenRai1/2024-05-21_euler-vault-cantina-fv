
/////////////////// METHODS START ///////////////////////
methods {
    //Harness functions
    function getHookTargetHarness() external returns (address) envfree;
    function useViewCallerHarness() external returns (address) envfree;
    function reentrancyLockedHarness() external returns (bool) envfree;

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
