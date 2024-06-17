import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////
    methods {
    //Harness functions
    function reentrancyLockedHarness() external returns (bool) envfree;
    function getCFG_MAX_VALUEHarness() external returns (uint32) envfree;
    function getOP_MAX_VALUEHarness() external returns (uint32) envfree;
    function toConfigAmountHarness(uint16 value) external returns (GovernanceHarness.ConfigAmount) envfree;
    function getCurrentLTVConfigHarness(address collateral) external returns (GovernanceHarness.LTVConfig) envfree;
    function getMAX_SANE_AMOUNTHarness() external returns (uint256) envfree;
    function wrapAmountCapHarness(uint16 value) external returns (GovernanceHarness.AmountCap) envfree;
    function resolveAmountCapHarness(GovernanceHarness.AmountCap self) external returns (uint256) envfree;
    function wrapFlagsHarness(uint32 value) external returns (GovernanceHarness.Flags) envfree;
    function isHookTarget() external returns (bytes4) envfree;
    function isValidInterestFeeHarness(uint16 interestFee) external returns (bool) envfree;
    function getGUARANTEED_INTEREST_FEE_MINHarness() external returns (uint16) envfree;
    function getGUARANTEED_INTEREST_FEE_MAXHarness() external returns (uint16) envfree;
    function getInterestRateHarness() external returns (uint72) envfree;
    function getUserStorageDataHarness(address user) external returns (GovernanceHarness.PackedUserSlot) envfree;
    function getGovernorReceiverHarness() external returns (address) envfree;
    function getTotalSharesHarness() external returns (GovernanceHarness.Shares) envfree;
    function getCurrentVaultCacheHarness() external returns (GovernanceHarness.VaultCache memory) envfree;
    function unpackBalanceHarness(GovernanceHarness.PackedUserSlot data) external returns (GovernanceHarness.Shares) envfree;

    //Governance functions
    function governorAdmin() external returns (address) envfree;
    function feeReceiver() external returns (address) envfree;
    function interestFee() external returns (uint16) envfree;
    function interestRateModel() external returns (address) envfree;
    function protocolConfigAddress() external returns (address) envfree;
    function protocolFeeShare() external returns (uint256) envfree;
    function protocolFeeReceiver() external returns (address) envfree;
    function caps() external returns (uint16, uint16) envfree;
    function LTVList() external returns (address[] memory) envfree;
    function maxLiquidationDiscount() external returns (uint16) envfree;
    function liquidationCoolOffTime() external returns (uint16) envfree;
    function hookConfig() external returns (address, uint32) envfree;
    function configFlags() external returns (uint32) envfree;
    function EVC() external returns (address) envfree;
    function unitOfAccount() external returns (address) envfree;
    function oracle() external returns (address) envfree;
    function permit2Address() external returns (address) envfree;
    function LTVFull(address collateral) external returns (uint16, uint16, uint16, uint48, uint32) envfree;
    function calculateProtocolFeeHarness(address governorReceiver, uint16 protocolFee) external returns (uint16) envfree;
    function interestRateHarness() external returns (uint72) envfree;


    function _.isHookTarget() external => NONDET;
    //Function summary


    function Cache.updateVault() internal returns (GovernanceHarness.VaultCache memory) with(env e) => CVLUpdateVault();

      

    }

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////

    definition GOVERNOR_ADMIN_ONLY_FUNCTIONS(method f) returns bool =
        f.selector == sig:clearLTV(address).selector ||
        f.selector == sig:setCaps(uint16,uint16).selector ||
        f.selector == sig:setConfigFlags(uint32).selector ||
        f.selector == sig:setFeeReceiver(address).selector ||
        f.selector == sig:setGovernorAdmin(address).selector ||
        f.selector == sig:setHookConfig(address,uint32).selector ||
        f.selector == sig:setInterestFee(uint16).selector ||
        f.selector == sig:setInterestRateModel(address).selector ||
        f.selector == sig:setLiquidationCoolOffTime(uint16).selector ||
        f.selector == sig:setLTV(address,uint16,uint16,uint32).selector ||
    f.selector == sig:setMaxLiquidationDiscount(uint16).selector;


    definition HARNESS_FUNCTIONS(method f) returns bool =
        f.selector == sig:getOnBehalfOfAccountHarness().selector ||
        f.selector == sig:getCFG_MAX_VALUEHarness().selector ||
        f.selector == sig:getOP_MAX_VALUEHarness().selector ||
        f.selector == sig:getMAX_SANE_AMOUNTHarness().selector ||
        f.selector == sig:toConfigAmountHarness(uint16 ).selector ||
        f.selector == sig:getLTVHarness(GovernanceHarness.LTVConfig memory, bool).selector ||
        f.selector == sig:getCurrentLTVConfigHarness(address ).selector ||
        f.selector == sig:wrapAmountCapHarness(uint16 ).selector ||
        f.selector == sig:resolveAmountCapHarness(GovernanceHarness.AmountCap).selector ||
        f.selector == sig:wrapFlagsHarness(uint32).selector ||
        f.selector == sig:unitOfAccount().selector ||
        f.selector == sig:vaultCacheOracleConfigured().selector ||
        f.selector == sig:vaultIsController(address).selector ||
        f.selector == sig:vaultIsOnlyController(address).selector ||
        f.selector == sig:getBalanceAndForwarderExt(address).selector ||
        f.selector == sig:getCollateralsExt(address).selector ||
        f.selector == sig:getLTVConfig(address).selector ||
        f.selector == sig:isAccountStatusCheckDeferredExt(address).selector ||
        f.selector == sig:isCollateralEnabledExt(address,address).selector ||
        f.selector == sig:isDepositDisabled().selector ||
        f.selector == sig:isMintDisabled().selector ||
        f.selector == sig:isOperationDisabledExt(uint32).selector ||
        f.selector == sig:isRedeemDisabled().selector ||
        f.selector == sig:isSkimDisabled().selector ||
        f.selector == sig:isWithdrawDisabled().selector ||
        f.selector == sig:calculateLiquidationLTVHarness(GovernanceHarness.LTVConfig,bool).selector ||
        f.selector == sig:calculateProtocolFeeHarness(address,uint16).selector ||
        f.selector == sig:calculateSharesToMoveHarness(GovernanceHarness.Shares,uint16).selector ||
        f.selector == sig:getCurrentVaultCacheHarness().selector ||
        f.selector == sig:getGUARANTEED_INTEREST_FEE_MAXHarness().selector ||
        f.selector == sig:getGUARANTEED_INTEREST_FEE_MINHarness().selector ||
        f.selector == sig:getGovernorReceiverHarness().selector ||
        f.selector == sig:getHookTargetSelectorHarness().selector ||
        f.selector == sig:getInterestRateHarness().selector ||
        f.selector == sig:getTargetInterestRateHarness(address,GovernanceHarness.VaultCache).selector ||
        f.selector == sig:getTotalSharesHarness().selector ||
        f.selector == sig:getUserStorageDataHarness(address).selector ||
        f.selector == sig:getVaultCacheHarness().selector ||
        f.selector == sig:isValidInterestFeeHarness(uint16).selector ||
        f.selector == sig:unpackBalanceHarness(GovernanceHarness.PackedUserSlot).selector ||
    f.selector == sig:reentrancyLockedHarness().selector;

    definition DISABLED_FUNCTIONS(method f) returns bool =
        f.selector == sig:isDepositDisabled().selector ||
        f.selector == sig:isMintDisabled().selector ||
        f.selector == sig:isOperationDisabledExt(uint32).selector ||
        f.selector == sig:isRedeemDisabled().selector ||
        f.selector == sig:isSkimDisabled().selector ||
    f.selector == sig:isWithdrawDisabled().selector;






///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////


    function CVLUpdateVault() returns GovernanceHarness.VaultCache {
        GovernanceHarness.VaultCache vaultCache = getCurrentVaultCacheHarness();
        return vaultCache;
    }
 


////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

//@audit-question-asked Do the hooks and ghost mappings work?
// //collateral address to borrowLTV
// ghost mapping(address => GovernanceHarness.ConfigAmount) ghostBorrowLTV;

// hook Sstore currentContract.vaultStorage.ltvLookup[KEY address collateral].borrowLTV GovernanceHarness.ConfigAmount newValue{
//     ghostBorrowLTV[collateral] = newValue;
// }

// hook Sload GovernanceHarness.ConfigAmount returnValue currentContract.vaultStorage.ltvLookup[KEY address collateral].borrowLTV{
//     require(ghostBorrowLTV[collateral] == returnValue);
// }

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////