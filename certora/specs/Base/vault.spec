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


        //Summaries
        function Cache.updateVault() internal returns (Type.VaultCache memory) with(env e) => CVLUpdateVaultAssumeNoUpdate();

        function _.increaseBalance(Type.VaultCache memory vaultCache, address account,address sender,Type.Shares amount, Type.Assets assets) internal => CVLIncreaseBalance(account, sender, amount, assets) expect void;

        function _.decreaseBalance(Type.VaultCache memory vaultCache, address account, address sender, address receiver, Type.Shares amount, Type.Assets assets) internal => CVLDecreaseBalance(account, sender, receiver, amount, assets) expect void;

        function _.decreaseAllowance(address owner, address spender, Type.Shares amount) internal => CVLDecreaseAllowance(owner, spender, amount) expect void;

        // function _.setAllowance(address owner, address spender, uint256 amount) internal => CVLSetAllowance(owner, spender, amount) expect void;

        function _.transferBalance(address from, address to, Type.Shares amount) internal => CVLTransferBalance(from, to, amount) expect void;

        // function _.transferFromMax(address from, address to) external =>
        //     CVLTransferFromMax(from, to) expect bool;


    
    }

/////////////////// METHODS END ///////////////////////

///////////////// DEFINITIONS START /////////////////////
    definition NONREENTRANT_FUNCTIONS (method f) returns bool = 
    f.selector == sig:mint(uint256,address).selector ||
    f.selector == sig:redeem(uint256,address,address).selector ||
    f.selector == sig:skim(uint256,address).selector ||
    f.selector == sig:deposit(uint256,address).selector ||
    f.selector == sig:approve(address,uint256).selector ||
    f.selector == sig:transfer(address,uint256).selector ||
    f.selector == sig:transferFrom(address,address,uint256).selector ||
    f.selector == sig:transferFromMax(address,address).selector ||
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
    f.selector == sig:allowance(address,address).selector ||
    f.selector == sig:balanceOf(address).selector ||
    f.selector == sig:totalSupply().selector ||
    f.selector == sig:totalAssets().selector;

    // definition VAULT_HARNESS_FUNCTIONS (method f) returns bool =





///////////////// DEFINITIONS END /////////////////////

////////////////// FUNCTIONS START //////////////////////

    // function CVLTransferFromMax(address from, address to) returns bool {
    //      validateTransferFromAccount(from);
    //      address account;
    //      bool notUsed;

    //     (notUsed, account) = initOperation(16, from);

    //     return transferFromInternal(account, from, to, shareAllowanceGhost[from]);
    // }

    function CVLTransferBalance(address from, address to, Type.Shares amount) {
        if (amount > 0) {
            // update from
            Type.Shares origFromBalance = shareBalanceGhost[from];
            require(to_mathint(origFromBalance) >= to_mathint(amount));
            Type.Shares newFromBalance = require_uint112(origFromBalance - amount);
            shareBalanceGhost[from] = newFromBalance;

            // update to
            Type.Shares origToBalance = shareBalanceGhost[to];
            require(origToBalance + amount <= max_uint112);
            Type.Shares newToBalance = require_uint112(origToBalance + amount);
            shareBalanceGhost[to] = newToBalance;
            
        }
        
    }

    function CVLSetAllowance(address owner, address spender, uint256 amount) {
        shareAllowanceGhost[owner][spender] = amount;
    }


    function CVLDecreaseAllowance (address owner, address spender, Type.Shares amount) {
        uint256 currentAllowance = shareAllowanceGhost[owner][spender];
        require(to_mathint(currentAllowance) >= to_mathint(amount));
        if(currentAllowance != max_uint256){
        uint256 newAllowance = assert_uint256(currentAllowance - amount);
        shareAllowanceGhost[owner][spender] = newAllowance;
        }
    }

    // owner => spender => allowance
    ghost mapping(address => mapping(address => uint256)) shareAllowanceGhost;


    function CVLIncreaseBalance(address account, address sender, Type.Shares amount, Type.Assets assets){
        // assert(account != 0); //commented out since only used for nonrevert tests
        //getUserBalance
        uint112 origBalance = shareBalanceGhost[account];
        require(origBalance + amount <= max_uint112);
        uint112 newBalance = assert_uint112(origBalance + amount);

        //setUserBalance
        shareBalanceGhost[account] = newBalance;

        //setTotalShares
        totalSharesGhost = totalSharesGhost + amount;
    }

    function CVLDecreaseBalance(address account, address sender, address receiver, Type.Shares amount, Type.Assets assets){
        // assert(account != 0); //commented out since only used for nonrevert tests
        //getUserBalance
        uint112 origBalance = shareBalanceGhost[account];
        require(to_mathint(origBalance) >= to_mathint(amount));
        uint112 newBalance = assert_uint112(origBalance - amount);

        //setUserBalance
        shareBalanceGhost[account] = newBalance;

        //setTotalShares
        totalSharesGhost = totalSharesGhost - amount;
    }
    
    ghost mapping(address => uint112) shareBalanceGhost{
        axiom forall address account. shareBalanceGhost[account] <= max_uint112 && shareBalanceGhost[account] >= 0;
    }

        
    ghost mathint totalSharesGhost{
        axiom totalSharesGhost <= max_uint112 && totalSharesGhost >= 0;
    }


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
