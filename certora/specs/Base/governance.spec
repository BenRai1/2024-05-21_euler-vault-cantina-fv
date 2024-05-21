

/////////////////// METHODS START ///////////////////////
methods {
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
function getCFG_MAX_VALUEHarness() external returns (uint32) envfree;
function getOP_MAX_VALUEHarness() external returns (uint32) envfree;
function toConfigAmountHarness(uint16 value) external returns (GovernanceHarness.ConfigAmount) envfree;




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



///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////



////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////