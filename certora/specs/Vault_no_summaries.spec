import "./Base.spec";
import "./GhostPow.spec";
import "./LoadVaultSummaries.spec";
import "./Base/vault_no_summaries.spec"; // does not have summary of increaseBalance

using VaultHarness as Vault;
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;


// used to test running time
use builtin rule sanity;


//------------------------------- RULES TEST START ----------------------------------












//transferFrom reverts



//transferFromMax reverts










//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------
    //withdraw reverts
    rule withdrawReverts(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address owner;
        require(owner != 1 && owner != 0);
        address onBehalfOf = actualCaller(e);
        Type.Shares sharesOfOwner = getUserBalanceHarness(owner);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address collateral = vaultCache.asset;
        require(collateral == VaultAsset);
        Type.Assets finalAssets = uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesUpHarness(finalAssets, vaultCache);
        bool flagIsNotSet = isNotSetCompatibeAssetHarness(vaultCache.configFlags);
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(receiver);

        bool checksDeferred = areChecksDeferredExt();
        uint256 numberOfControlers = EVC.accountControllers[owner].numElements;



        //VALUES BEFORE

        //FUNCTION CALL
        withdraw@withrevert(e, amount, receiver, owner);

        //VALUES AFTER

        //ASSERTS
        // // assert5: flag is not set && isKnownNonOwnerAccount, then function should revert //@audit  time out
        // assert(finalAssets != 0 && flagIsNotSet && isKnownNonOwnerAccount => lastReverted, "flag is not set && isKnownNonOwnerAccount: Function call should revert");


        // // assert7: if sharesOfOwner < finalShares, then function should revert //@audit time out
        assert(finalAssets != 0 && sharesOfOwner < finalShares => lastReverted, "sharesOfOwner < finalShares: Function call should revert");

        //--------------Asserts OK Start----------------

            // //assert1: if e.msg.sender != ENV, then function should revert
            // assert(e.msg.sender != EVC => lastReverted, "e.msg.sender != ENV: Function call should revert");

            // //assert2: if onBehalfOf == 0, then function should revert
            // assert(onBehalfOf == 0 => lastReverted, "onBehalfOf == 0: Function call should revert");



            // //assert3: if vaultCashe.cash < finalAssets, then function should revert
            // assert(finalAssets != 0 && vaultCache.cash < finalAssets => lastReverted, "vaultCashe.cash < finalAssets: Function call should revert");

            // // assert4: if receiver == 0, then function should revert
            // assert(finalAssets != 0 && receiver == 0 => lastReverted, "receiver == 0: Function call should revert");

            // // assert6: if !checksDeferred && numberOfControlers > 1, then function should revert
            // assert(finalAssets != 0 && !checksDeferred && numberOfControlers > 1 => lastReverted, "!checksDeferred && numberOfControlers > 1: Function call should revert");

        //--------------Asserts OK End----------------

    }

    //redeem reverts
    rule redeemReverts(env e){
        //FUNCTION PARAMETER
        uint256 amount; //i: shares to be redeemed
        address receiver;
        address owner;
        require(owner != 1 && owner != 0);
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address collateral = vaultCache.asset;
        require(collateral == VaultAsset);
        Type.Shares sharesOfOwner = getUserBalanceHarness(owner);

        //Final Values
        Type.Shares finalShares = amount == max_uint256 ? sharesOfOwner : uintToSharesHarness(amount);
        Type.Assets finalAssets = sharesToAssetsDownHarness(finalShares, vaultCache);
        bool flagIsNotSet = isNotSetCompatibeAssetHarness(vaultCache.configFlags);
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(receiver);

        bool checksDeferred = areChecksDeferredExt();
        uint256 numberOfControlers = getControlersExt(owner).length;



        //VALUES BEFORE

        //FUNCTION CALL
        redeem@withrevert(e, amount, receiver, owner);

        //VALUES AFTER

        //ASSERTS
        // //assert3: if vaultCashe.cash < finalAssets, then function should revert //@audit time out
        // assert(finalShares != 0 && vaultCache.cash < finalAssets => lastReverted, "vaultCashe.cash < finalAssets: Function call should revert");

        // assert5: flag is not set && isKnownNonOwnerAccount, then function should revert //@audit time out
        assert(finalShares != 0 && flagIsNotSet && isKnownNonOwnerAccount => lastReverted, "flag is not set && isKnownNonOwnerAccount: Function call should revert");





        //-----------------Asserts OK Start-----------------
            // //assert1: if e.msg.sender != ENV, then function should revert
            // assert(e.msg.sender != EVC => lastReverted, "e.msg.sender != ENV: Function call should revert");

            // //assert2: if onBehalfOf == 0, then function should revert 
            // assert(onBehalfOf == 0 => lastReverted, "onBehalfOf == 0: Function call should revert");


            // // assert4: if receiver == 0, then function should revert
            // assert(finalShares != 0 && receiver == 0 => lastReverted, "receiver == 0: Function call should revert");

            // // assert6: if !checksDeferred && numberOfControlers > 1, then function should revert
            // assert(finalShares != 0 && !checksDeferred && numberOfControlers > 1 => lastReverted, "!checksDeferred && numberOfControlers > 1: Function call should revert");

            // // assert7: if origBalance < finalShares, then function should revert 
            // assert(finalShares != 0 && sharesOfOwner < finalShares => lastReverted, "origBalance < finalShares: Function call should revert");

            // // assert8: if finalAssets = 0, then function should revert
            // assert(finalShares !=0 && finalAssets == 0 => lastReverted, "finalAssets == 0: Function call should revert");

        //-----------------Asserts OK End-----------------

    }

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------


    //transferFromMax reverts
    rule transferFromMaxReverts(env e){
        //FUNCTION PARAMETER
        address to;
        address from;
        Type.Shares sharesOfFrom = getUserBalanceHarness(from);
        address spender = actualCaller(e);
        require(from != spender);
        //VALUES BEFORE
        uint256 allowance = getETokenAllowanceHarness(from, spender);

        //FUNCTION CALL
        transferFromMax@withrevert(e, from, to);
        bool reverted = lastReverted;

        //ASSERTS
        //assert0: if from == 1, then function should revert (CHECKACCOUNT_CALLER)
        assert(from == 1 => reverted, "from == 1: Function call should revert");
        
        //assert1: if from == 0, then function should revert (CHECKACCOUNT_NONE)
        assert(from == 0 => reverted, "from == 0: Function call should revert");

        //assert2: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert3: if to == from the function should revert
        assert(to == from => reverted, "to == from: Function call should revert");

        //assert4: if to == 0, then function should revert
        assert(to == 0 => reverted, "to == 0: Function call should revert");

        //assert5: if allowanceSpender < amount, then function should revert
        assert(to_mathint(allowance) < to_mathint(sharesOfFrom) => reverted, "allowance < amount: Function call should revert");
    }

    //transferFrom reverts
    rule transferFromReverts(env e){
        //FUNCTION PARAMETER
        address to;
        uint256 amount;
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address from;
        Type.Shares sharesOfFrom = getUserBalanceHarness(from);
        address spender = actualCaller(e);
        require(from != spender);
        //VALUES BEFORE
        uint256 allowance = getETokenAllowanceHarness(from, spender);

        //FUNCTION CALL
        transferFrom@withrevert(e, from, to, amount);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert0: if from == 1, then function should revert (CHECKACCOUNT_CALLER)
        assert(from == 1 => reverted, "from == 1: Function call should revert");
        
        //assert1: if from == 0, then function should revert (CHECKACCOUNT_NONE)
        assert(from == 0 => reverted, "from == 0: Function call should revert");

        //assert2: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert3: if to == from the function should revert
        assert(to == from => reverted, "to == from: Function call should revert");

        //assert4: if to == 0, then function should revert
        assert(to == 0 => reverted, "to == 0: Function call should revert");

        //assert5: if amountInShares > sharesOfFrom, then function should revert
        assert(amountInShares > sharesOfFrom => reverted, "amountInShares > sharesOfFrom: Function call should revert");

        //assert6: if allowanceSpender < amount, then function should revert
        assert(allowance < amount => reverted, "allowance < amount: Function call should revert");
    }

    //transfer reverts
    rule transferReverts(env e){
        //FUNCTION PARAMETER
        address to;
        uint256 amount;
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address from = actualCaller(e);
        Type.Shares sharesOfFrom = getUserBalanceHarness(from);
        //VALUES BEFORE

        //FUNCTION CALL
        transfer@withrevert(e, to, amount);
        bool reverted = lastReverted;


        //VALUES AFTER

        //ASSERTS
        //assert1: if from == 0, then function should revert
        assert(from == 0 => reverted, "from == 0: Function call should revert");

        //assert2: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert3: if to == from the function should revert
        assert(to == from => reverted, "to == from: Function call should revert");

        //assert4: if to == 0, then function should revert
        assert(to == 0 => reverted, "to == 0: Function call should revert");

        //assert5: if amountInShares > sharesOfFrom, then function should revert
        assert(amountInShares > sharesOfFrom => reverted, "amountInShares > sharesOfFrom: Function call should revert");

    }

    //skim reverts
    rule skimReverts(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address collateral = vaultCache.asset;
        require(collateral == VaultAsset);

        //VALUES BEFORE
        Type.Assets balanceVault = uintToAssetsHarness(VaultAsset.balanceOf(e, currentContract));
        Type.Assets assetsAvailable = balanceVault <= vaultCache.cash ? 0 : uintToAssetsHarness(require_uint256(balanceVault - vaultCache.cash));

        //FINAL VALUES
        Type.Assets finalAssets = amount == max_uint256 ? assetsAvailable : uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCache);


        //FUNCTION CALL
        skim@withrevert(e, amount, receiver);

        //VALUES AFTER

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => lastReverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => lastReverted, "onBehalfOf == 0: Function call should revert");

        //assert3: if finalAssets > availableAssets, then function should revert
        assert(finalAssets > assetsAvailable => lastReverted, "finalAssets > availableAssets: Function call should revert");

        //assert4: if finalShares == 0, then function should revert
        assert(finalAssets != 0 && finalShares == 0 => lastReverted, "finalShares == 0: Function call should revert");

        //assert5: if receiver == 0, then function should revert
        assert(finalAssets != 0 && receiver == 0 => lastReverted, "receiver == 0: Function call should revert");
    }

    //mint reverts
    rule mintReverts(env e){ 
        //FUNCTION PARAMETER
        uint256 amount; //i: shares to be minted
        address receiver;
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address collateral = vaultCache.asset;
        require(collateral == VaultAsset); 
        uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e,onBehalfOf);

        //FINAL VALUES
        Type.Shares finalShares = uintToSharesHarness(amount);
        Type.Assets finalAssets = shareToAssetsUpHarness(finalShares, vaultCache);
        uint256 finalAssetsUint = assetsToUintHarness(finalAssets);


        //VALUES BEFORE

        //FUNCTION CALL
        mint@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => reverted, "onBehalfOf == 0: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(finalShares != 0 && receiver == 0 => reverted, "receiver == 0: Function call should revert");
    }
   
    //deposit reverts
    rule depositReverts(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address onBehalfOf = actualCaller(e);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address collateral = vaultCache.asset;
        require(collateral == VaultAsset); 
        uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e,onBehalfOf);

        Type.Assets assets = 
        amount == max_uint256 ? 
        uintToAssetsHarness(balanceOnBehalfOfBefore) : uintToAssetsHarness(amount);
        Type.Shares shares = assetsToSharesDownHarness(assets, vaultCache);

        //VALUES BEFORE

        //FUNCTION CALL
        deposit@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //VALUES AFTER

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => reverted, "onBehalfOf == 0: Function call should revert");

        //assert3: if amount == 0, then function should revert
        assert(assets != 0 && shares == 0 => reverted, "amount == 0: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(assets != 0 && receiver == 0 => reverted, "receiver == 0: Function call should revert");
    }

    //nonReentrant modifier works
    rule nonReentrantWorks(env e, method f, calldataarg args) filtered{
        f-> NONREENTRANT_FUNCTIONS(f)
    }{
        //VALUES BEFORE
        bool reentrancyLocked = Vault.vaultStorage.reentrancyLocked;

        //FUNCTION CALL
        f@withrevert(e, args);

        //ASSERTS
        assert(reentrancyLocked => lastReverted, "Function call should revert");

    }

        //nonReentrantView modifier works
    rule nonReentrantViewWorks(env e, method f, calldataarg args) filtered{
        f-> NONREENTRANTVIEW_FUNCTIONS(f)
    }{
        //VALUES BEFORE
        bool reentrancyLocked = Vault.vaultStorage.reentrancyLocked;
        address hookTarget = Vault.vaultStorage.hookTarget;
        bool shouldRevert = e.msg.sender != hookTarget && !(e.msg.sender == currentContract && CVLuseViewCaller() == hookTarget);

        //FUNCTION CALL
        f@withrevert(e, args);
        bool reverted = lastReverted;

        //ASSERTS
        assert(reentrancyLocked && shouldRevert => reverted, "Function call should revert");
    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------




