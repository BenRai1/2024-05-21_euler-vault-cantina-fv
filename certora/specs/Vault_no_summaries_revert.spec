import "./Base.spec";
import "./GhostPow.spec";
import "./LoadVaultSummaries.spec";
import "./Base/vault_no_summaries_revert.spec"; // does not have summary of increaseBalance

using VaultHarness as Vault;
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;


// used to test running time
use builtin rule sanity;


//------------------------------- RULES OK START ------------------------------------

   
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
        bool opSet = isRedeemSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();

        //Final Values
        Type.Shares finalShares = amount == max_uint256 ? sharesOfOwner : uintToSharesHarness(amount);
        Type.Assets finalAssets = sharesToAssetsDownHarness(finalShares, vaultCache);
        bool flagIsNotSet = isNotSetCompatibeAssetHarness(vaultCache.configFlags);
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(receiver);

        bool checksDeferred = areChecksDeferredExt();
        uint256 numberOfControlers = getControlersExt(owner).length;

        //FUNCTION CALL
        redeem@withrevert(e, amount, receiver, owner);

        // ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => lastReverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert 
        assert(onBehalfOf == 0 => lastReverted, "onBehalfOf == 0: Function call should revert");

        //assert3: if vaultCashe.cash < finalAssets, then function should revert
        assert(finalShares != 0 && vaultCache.cash < finalAssets => lastReverted, "vaultCashe.cash < finalAssets: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(finalShares != 0 && receiver == 0 => lastReverted, "receiver == 0: Function call should revert");

        // assert5: flag is not set && isKnownNonOwnerAccount, then function should revert
        assert(finalShares != 0 && flagIsNotSet && isKnownNonOwnerAccount => lastReverted, "flag is not set && isKnownNonOwnerAccount: Function call should revert");

        // assert6: if !checksDeferred && numberOfControlers > 1, then function should revert
        assert(finalShares != 0 && !checksDeferred && numberOfControlers > 1 => lastReverted, "!checksDeferred && numberOfControlers > 1: Function call should revert");

        // assert7: if origBalance < finalShares, then function should revert 
        assert(finalShares != 0 && sharesOfOwner < finalShares => lastReverted, "origBalance < finalShares: Function call should revert");

        // assert8: if finalAssets = 0, then function should revert
        assert(finalShares !=0 && finalAssets == 0 => lastReverted, "finalAssets == 0: Function call should revert");

        //assert9: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => lastReverted, "opSet and hookTarget is 0 => Function should revert");

    }

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
        bool opSet = isWithdrawSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();

        //FUNCTION CALL
        withdraw@withrevert(e, amount, receiver, owner);

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => lastReverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => lastReverted, "onBehalfOf == 0: Function call should revert");

        //assert3: if vaultCashe.cash < finalAssets, then function should revert
        assert(finalAssets != 0 && vaultCache.cash < finalAssets => lastReverted, "vaultCashe.cash < finalAssets: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(finalAssets != 0 && receiver == 0 => lastReverted, "receiver == 0: Function call should revert");

        // assert5: flag is not set && isKnownNonOwnerAccount, then function should revert
        assert(finalAssets != 0 && flagIsNotSet && isKnownNonOwnerAccount => lastReverted, "flag is not set && isKnownNonOwnerAccount: Function call should revert");

        // assert6: if !checksDeferred && numberOfControlers > 1, then function should revert
        assert(finalAssets != 0 && !checksDeferred && numberOfControlers > 1 => lastReverted, "!checksDeferred && numberOfControlers > 1: Function call should revert");

        // assert7: if sharesOfOwner < finalShares, then function should revert 
        assert(finalAssets != 0 && sharesOfOwner < finalShares => lastReverted, "sharesOfOwner < finalShares: Function call should revert");

        //assert8: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => lastReverted, "opSet and hookTarget is 0 => Function should revert");

    }

    //transfer reverts
    rule transferReverts(env e){
        //FUNCTION PARAMETER
        address to;
        uint256 amount;
        Type.Shares amountInShares = uintToSharesHarness(amount);
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        address from = actualCaller(e);
        Type.Shares sharesOfFrom = getUserBalanceHarness(from);
        //VALUES BEFORE
        bool opSet = isTransferSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();


        //FUNCTION CALL
        transfer@withrevert(e, to, amount);
        bool reverted = lastReverted;

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

        //assert6:  if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

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
        bool opSet = isSkimSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();


        //FINAL VALUES
        Type.Assets finalAssets = amount == max_uint256 ? assetsAvailable : uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCache);

        //FUNCTION CALL
        skim@withrevert(e, amount, receiver);

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

        //assert6: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => lastReverted, "opSet and hookTarget is 0 => Function should revert");

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
        bool opSet = isMintSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();



        //FUNCTION CALL
        mint@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => reverted, "onBehalfOf == 0: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(finalShares != 0 && receiver == 0 => reverted, "receiver == 0: Function call should revert");

        //assert5: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

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
        bool opSet = isDepositSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();


        //FUNCTION CALL
        deposit@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if e.msg.sender != ENV, then function should revert
        assert(e.msg.sender != EVC => reverted, "e.msg.sender != ENV: Function call should revert");

        //assert2: if onBehalfOf == 0, then function should revert
        assert(onBehalfOf == 0 => reverted, "onBehalfOf == 0: Function call should revert");

        //assert3: if amount == 0, then function should revert
        assert(assets != 0 && shares == 0 => reverted, "amount == 0: Function call should revert");

        // assert4: if receiver == 0, then function should revert
        assert(assets != 0 && receiver == 0 => reverted, "receiver == 0: Function call should revert");

        //assert5: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

    }


//------------------------------- RULES OK END ------------------------------------

//--------------------------------- PUBLIC MUTATION START-----------------------

    //   //skim works
    //     rule skimPublicMutation(env e){
    //         //FUNCTION PARAMETER
    //         uint256 amount;
    //         require(amount == max_uint256);//@audit to be able to see valid run
    //         // uint256 MAX_SANE_AMOUNT = getMAX_SANE_AMOUNT(e);
    //         // assert(MAX_SANE_AMOUNT == amount); //@audit MAX_SANE_AMOUNT is set to max_uint112
    //         address receiver;

    //         //Requirements
    //         Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
    //         address collateral = vaultCacheBefore.asset;
    //         require(collateral == VaultAsset);
    //         //VALUES BEFORE
    //         Type.Assets cashBefore = vaultCacheBefore.cash;
    //         uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);
    //         //Target values
    //         Type.Assets amountChange = amount == max_uint256 ? uintToAssetsHarness(balanceVaultBefore) : uintToAssetsHarness(amount);

    //         //FUNCTION CALL
    //         skim@withrevert(e, amount, receiver);

    //         //VALUES AFTER
    //         Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
    //         Type.Assets cashAfter = vaultCacheAfter.cash;


    //         //ASSERTS
    //         //assert1: cash should increase by amountChange
    //         assert(cashBefore + amountChange == to_mathint(cashAfter), "Cash should increase by amountChange");
    //         assert(false);




            
    //         // Type.Assets cashBefore = vaultCacheBefore.cash;

    //         // //VALUES BEFORE
    //         // mathint totalSharesBefore = totalSharesGhost;
    //         // mathint sharesReceiverBefore = shareBalanceGhost[receiver];
    //         // mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
    //         // //Balances before
    //         // uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);
    //         // require(balanceVaultBefore != 0);//@audit to be able to see valid run
    //         // Type.Assets assetsAvailable = to_mathint(balanceVaultBefore) <= to_mathint(vaultCacheBefore.cash) ? 0 : uintToAssetsHarness(require_uint256(balanceVaultBefore - vaultCacheBefore.cash));

    //         // //FINAL VALUES
    //         // Type.Assets finalAssets = amount == max_uint256 ? assetsAvailable : uintToAssetsHarness(amount);
    //         // Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCacheBefore);

    //         // //FUNCTION CALL
    //         // uint256 returnValueCall = skim(e, amount, receiver);

    //         // //VALUES AFTER
    //         // Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
    //         // //Balances after
    //         // uint256 balanceVaultAfter = VaultAsset.balanceOf(e,currentContract);
    //         // uint256 balanceReceiverAfter = VaultAsset.balanceOf(e,receiver);
    //         // uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
    //         // mathint totalSharesAfter = totalSharesGhost;
    //         // mathint sharesReceiverAfter = shareBalanceGhost[receiver];
    //         // mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];

    //         // //ASSERTS
    //         // //assert5: finalAssets !=0 => vaultChash should be increased by finalAssets
    //         // assert(finalAssets != 0 => vaultCacheBefore.cash + finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should increase by finalAssets");

    //         // assert(false);


    //         // //assert6: finalAssets !=0 => totalShares should increase by finalShares
    //         // assert(finalAssets != 0 => totalSharesBefore + finalShares == to_mathint(totalSharesAfter), "Total shares should increase by finalShares");

    //         // //assert7: finalAssets !=0 => receiverShares should be increased by finalShares
    //         // assert(finalAssets != 0 => sharesReceiverBefore + finalShares == to_mathint(sharesReceiverAfter), "Shares of receiver should increase by finalShares");

    //         // //assert8: otherUserShares should stay the same
    //         // assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should stay the same");
    //     }

//--------------------------------- PUBLIC MUTATION END-----------------------





