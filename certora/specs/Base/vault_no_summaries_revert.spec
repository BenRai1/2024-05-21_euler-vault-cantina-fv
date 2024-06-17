import "./abstractBase.spec";

/////////////////// METHODS START ///////////////////////


    methods {
        function name() external returns string envfree;
        function symbol() external returns string envfree;
        function decimals() external returns uint8 envfree;
        function asset() external returns address envfree;
        function approve(address,uint256) external returns bool;
        function deposit(uint256,address) external;
        function mint(uint256,address) external;
        function withdraw(uint256,address,address) external;
        function redeem(uint256,address,address) external;
        function permit(address,address,uint256,uint256,uint8,bytes32,bytes32) external;
        function DOMAIN_SEPARATOR() external returns bytes32;

        /// Summaries
        // summary for rpow
        function RPow.rpow(uint256 x, uint256 y, uint256 base) internal returns (uint256, bool) => CVLPow(x, y, base);

        function _.useViewCaller() internal => CVLuseViewCaller() expect address;

        // See comment near CVLgetCurrentOnBehalfOfAccount definition in LoadVaultSummaries spec.
        function _.getCurrentOnBehalfOfAccount(address controller) external => CVLgetCurrentOnBehalfOfAccount(controller) expect (address, bool);

        function storage_lastInterestAccumulatorUpdate() external returns (uint48) envfree;
        function storage_cash() external returns (VaultHarness.Assets) envfree;
        function storage_supplyCap() external returns (uint256) envfree;
        function storage_borrowCap() external returns (uint256) envfree;
        function storage_hookedOps() external returns (VaultHarness.Flags) envfree;
        function storage_snapshotInitialized() external returns (bool) envfree;
        function storage_totalShares() external returns (VaultHarness.Shares) envfree;
        function storage_totalBorrows() external returns (VaultHarness.Owed) envfree;
        function storage_accumulatedFees() external returns (VaultHarness.Shares) envfree;
        function storage_interestAccumulator() external returns (uint256) envfree;
        function storage_configFlags() external returns (VaultHarness.Flags) envfree;
        function getCurrentVaultCacheHarness() external returns (Type.VaultCache memory) envfree;
        function getUserBalanceHarness(address user) external returns (Type.Shares) envfree;
        function getETokenAllowanceHarness(address user, address spender) external returns (uint256) envfree;
        function userAssets(address user) external returns(uint256) envfree;


        //Summaries
        function Cache.updateVault() internal returns (Type.VaultCache memory) with(env e) => CVLUpdateVaultAssumeNoUpdate();

        function Base.invokeHookTarget(address caller) internal with (env e)=> InvokeHookHarness(e);

    
    }

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////
    definition NONREENTRANT_FUNCTIONS (method f) returns bool = 
    f.selector == sig:mint(uint256,address).selector ||
    f.selector == sig:redeem(uint256,address,address).selector ||
    f.selector == sig:skim(uint256,address).selector ||
    f.selector == sig:deposit(uint256,address).selector ||
    f.selector == sig:withdraw(uint256,address,address).selector;

    definition NONREENTRANTVIEW_FUNCTIONS (method f) returns bool =
    f.selector == sig:accumulatedFeesAssets().selector ||
    f.selector == sig:convertToAssets(uint256).selector ||
    f.selector == sig:convertToShares(uint256).selector ||
    f.selector == sig:maxDeposit(address).selector ||
    f.selector == sig:maxMint(address).selector ||
    f.selector == sig:maxRedeem(address).selector ||
    f.selector == sig:maxWithdraw(address).selector ||
    f.selector == sig:previewDeposit(uint256).selector ||
    f.selector == sig:previewMint(uint256).selector ||
    f.selector == sig:previewRedeem(uint256).selector ||
    f.selector == sig:previewWithdraw(uint256).selector ||
    f.selector == sig:accumulatedFees().selector ||
    f.selector == sig:totalAssets().selector;





///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////

    function CVLUpdateVaultAssumeNoUpdate() returns Type.VaultCache {
            Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
            return vaultCache;
    }

    function CVLuseViewCaller() returns address {
        return viewCallerGhost;
    }

    ghost address viewCallerGhost;


    function CVLgetCurrentOnBehalfOfAccount(address addr) returns (address, bool) {
        return (CVLgetCurrentOnBehalfOfAccountAddr(addr),
            CVLgetCurrentOnBehalfOfAccountBool(addr));
    }

    // Assumptions for LTVConfig
    function LTVConfigAssumptions(env e, VaultHarness.LTVConfig ltvConfig) returns bool {
        bool LTVLessOne = ltvConfig.liquidationLTV < 10000;
        bool initialLTVLessOne = ltvConfig.initialLiquidationLTV < 10000;
        bool target_less_original = ltvConfig.liquidationLTV < ltvConfig.initialLiquidationLTV;
        mathint timeRemaining = ltvConfig.targetTimestamp - e.block.timestamp;
        return LTVLessOne &&
            initialLTVLessOne &&
            target_less_original && 
            require_uint32(timeRemaining) < ltvConfig.rampDuration;
    }


////////////////// FUNCTIONS END //////////////////////

///////////////// GHOSTS & HOOKS START //////////////////
// This is not in the scene for this config, so we just want it to be
// an uninterpreted function rather than NONDET so that
// we get the same value when this is called for different parts
ghost CVLgetCurrentOnBehalfOfAccountAddr(address) returns address;
ghost CVLgetCurrentOnBehalfOfAccountBool(address) returns bool;

///////////////// GHOSTS & HOOKS END //////////////////

///////////////// INITIAL PROPERTIES START /////////////

///////////////// INITIAL PROPERTIES END /////////////
