import "./Base.spec";
import "./GhostPow.spec";
import "./LoadVaultSummaries.spec";
import "./Base/vault_no_summaries.spec"; // does not have summary of increaseBalance

using VaultHarness as Vault;
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;


// used to test running time
use builtin rule sanity;


//------------------------------- RULES OK START ------------------------------------

    //asset works
    rule v_assetWorks(env e){
        //Storage values
        address assetStorage = getAssetHarness(e);

        //FUNCTION CALL
        address asset = asset(e);

        //ASSERTS
        //assert1: asset should be the same as the storage value
        assert(asset == assetStorage, "asset should be the same as the storage value");
    }

    //accumulatedFeesAssets works
    rule v_accumulatedFeesAssetsWorks(env e){
        //Storage values
        Type.VaultCache vaultCache = getCurrentVaultCacheHarness();
        Type.Assets accumulatedFeesStorageAssets = sharesToAssetsDownHarness(Vault.vaultStorage.accumulatedFees, vaultCache);
        uint256 accumulatedFeesStorageAssetsInUint = assetsToUintHarness(accumulatedFeesStorageAssets);

        //FUNCTION CALL
        uint256 accumulatedFeesAssets = accumulatedFeesAssets(e);

        //ASSERTS
        //assert1: accumulatedFeesAssets should be the same as the storage value
        assert(accumulatedFeesAssets == accumulatedFeesStorageAssetsInUint, "accumulatedFeesAssets should be the same as the storage value");
    }

    //creator works
    rule v_creatorWorks(env e){
        //Storage values
        address creatorStorage = Vault.vaultStorage.creator;

        //FUNCTION CALL
        address creator = creator(e);

        //ASSERTS
        //assert1: creator should be the same as the storage value
        assert(creator == creatorStorage, "creator should be the same as the storage value");
    }

    //totalAssets works
    rule v_totalAssetsWorks(env e){
        //Storage values
        uint256 cash = assetsToUintHarness(Vault.vaultStorage.cash);
        Type.Assets owedInAssets = owedToAssetsUpHarness(Vault.vaultStorage.totalBorrows);
        mathint totalAssetsStorage = assetsToUintHarness(owedInAssets) + cash;

        //FUNCTION CALL
        mathint totalAssets = totalAssets(e);

        //ASSERTS
        //assert1: totalAssets should be the same as the storage value
        assert(totalAssets == totalAssetsStorage, "totalAssets should be the same as the storage value");
    }

    //accumulatedFees works
    rule v_accumulatedFeesWorks(env e){
        //Storage values
        uint256 accumulatedFeesStorage = sharesToUintHarness(Vault.vaultStorage.accumulatedFees);

        //FUNCTION CALL
        uint256 accumulatedFees = accumulatedFees(e);

        //ASSERTS
        //assert1: accumulatedFees should be the same as the storage value
        assert(accumulatedFees == accumulatedFeesStorage, "accumulatedFees should be the same as the storage value");
    }

    //previewDeposit should be equal to the deposit
    rule v_previewDepositEqualDeposit(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;

        //FUNCTION CALL
        uint256 returnValuePreview = previewDeposit(e, amount);
        uint256 returnValueCall = deposit(e, amount, receiver);

        //ASSERTS
        assert(returnValuePreview == returnValueCall, "PreviewDeposit should be equal to the deposit");
    }

    //previewMint should be equal to the mint
    rule v_previewMintEqualMint(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;

        //FUNCTION CALL
        uint256 returnValuePreview = previewMint(e, amount);
        uint256 returnValueCall = mint(e, amount, receiver);

        //ASSERTS
        assert(returnValuePreview == returnValueCall, "PreviewMint should be equal to the mint");
    }

    //previewRedeem should be equal to the redeem
    rule v_previewRedeemEqualRedeem(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address owner;

        //FUNCTION CALL
        uint256 returnValuePreview = previewRedeem(e, amount);
        uint256 returnValueCall = redeem(e, amount, receiver, owner);

        //ASSERTS
        assert(returnValuePreview == returnValueCall, "PreviewRedeem should be equal to the redeem");
    }

    //previewWithdraw should be equal to the withdraw
    rule v_previewWithdrawEqualWithdraw(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address owner;

        //FUNCTION CALL
        uint256 returnValuePreview = previewWithdraw(e, amount);
        uint256 returnValueCall = withdraw(e, amount, receiver, owner);

        //ASSERTS
        assert(returnValuePreview == returnValueCall, "PreviewWithdraw should be equal to the withdraw");
    }

    //maxDeposit should be depositable
    rule v_maxDepositShouldBeDepositable(env e){
        //FUNCTION PARAMETER
        address account;

        //FUNCTION CALL
        uint256 maxMint = maxMint(e, account);
        mint(e, maxMint, account);

        //ASSERTS
        assert(true);
    }

    //maxMint should be mintable
    rule v_maxMintShouldBeMintable(env e){
        //FUNCTION PARAMETER
        address account;

        //FUNCTION CALL
        uint256 maxMint = maxMint(e, account);
        mint(e, maxMint, account);

        //ASSERTS
        assert(true);
    }

    //maxRedeem should be redeemable
    rule v_maxRedeemShouldBeRedeemable(env e){
        //FUNCTION PARAMETER
        address account;

        //FUNCTION CALL
        uint256 maxRedeem = maxRedeem(e, account);
        redeem(e, maxRedeem, account, account);

        //ASSERTS
        assert(true);
    }

    //maxWithdraw should be withdrawable
    rule v_maxWithdrawShouldBeWithdrawable(env e){
        //FUNCTION PARAMETER
        address account;

        //FUNCTION CALL
        uint256 maxWithdraw = maxWithdraw(e, account);
        withdraw(e, maxWithdraw, account, account);

        //ASSERTS
        assert(true);
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
        bool isRedeemDisabled = isRedeemDisabled(e);

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

        // assert9: if isRedeemDisabled, then function should revert
        assert(isRedeemDisabled => lastReverted, "isRedeemDisabled: Function call should revert");
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
        bool isWithdrawDisabled = isWithdrawDisabled(e);

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

        // assert8: if isWithdrawDisabled, then function should revert
        assert(isWithdrawDisabled => lastReverted, "isWithdrawDisabled: Function call should revert");
    }

    //only functions to increase the assets of a user
    rule onlyIncreaseUserAssets(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        address user;
        require(user != Vault);
        uint256 assetsBefore = userAssets(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = userAssets(user);

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(assetsBefore < assetsAfter =>
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to increase the user assets");
    }

    //only functions to decrease the assets of a user
    rule onlyDecreaseUserAssets(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        address user;
        require(user != Vault);
        uint256 assetsBefore = userAssets(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 assetsAfter = userAssets(user);

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(assetsBefore > assetsAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:skim(uint256,address).selector,
        "This function should not be able to decrease the user assets");
    }

    //only functions to increase the vault cash
    rule onlyIncreaseVaultCash(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        Type.Assets cashBefore = getCurrentVaultCacheHarness().cash;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Assets cashAfter = getCurrentVaultCacheHarness().cash;

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(cashBefore < cashAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:skim(uint256,address).selector,
        "This function should not be able to change the vault cash");
    }

    //only functions to decrease the vault cash
    rule onlyDecreaseVaultCash(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        Type.Assets cashBefore = getCurrentVaultCacheHarness().cash;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Assets cashAfter = getCurrentVaultCacheHarness().cash;

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(cashBefore > cashAfter =>
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the vault cash");
    }

    //only functions to increase user shares
    rule onlyIncreaseUserShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        address user;
        Type.Shares sharesBefore = getUserBalanceHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares sharesAfter = getUserBalanceHarness(user);

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(sharesBefore < sharesAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:transfer(address,uint256).selector ||
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:transferFromMax(address,address).selector ||
        f.selector == sig:skim(uint256,address).selector,
        "This function should not be able to increase the user shares");
    }

    //only functions to decrease user shares
    rule onlyDecreaseUserShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        address user;
        Type.Shares sharesBefore = getUserBalanceHarness(user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares sharesAfter = getUserBalanceHarness(user);

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(sharesBefore > sharesAfter =>
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector ||
        f.selector == sig:transfer(address,uint256).selector ||
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:transferFromMax(address,address).selector,
        "This function should not be able to decrease the user shares");
    }

    //only functions to increase the total supply of shares
    rule onlyIncreaseTotalSupplyOfShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
        } {
        //VALUES BEFORE
        mathint totalSharesBefore = storage_totalShares();

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        mathint totalSharesAfter = storage_totalShares();

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(totalSharesBefore < totalSharesAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:skim(uint256,address).selector,
        "This function should not be able to change the user shares");
    }

    //only functions to decreas the total supply of shares
    rule onlyDecreaseTotalSupplyOfShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        mathint totalSharesBefore = storage_totalShares();

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        mathint totalSharesAfter = storage_totalShares();

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(totalSharesBefore > totalSharesAfter =>
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the user shares");
    }

    //transferFromMax works
    rule transferFromMaxWorks(env e){
        //FUNCTION PARAMETER
        address from;
        address to;
        address otherUser;
        Type.Shares finalShares = getUserBalanceHarness(from);
        address onBahalfOf = actualCaller(e); //i: onBahalfOf  address
        require(otherUser != from && otherUser != onBahalfOf && otherUser != to);
        require(from != to && from != onBahalfOf);

        //VALUES BEFORE
        //shares before
        Type.Shares sharesFromBefore = getUserBalanceHarness(from);
        Type.Shares sharesToBefore = getUserBalanceHarness(to);
        Type.Shares sharesotherUserBefore = getUserBalanceHarness(otherUser);

        //allowance before
        uint256 allowanceOtherUserForOnBehalfOfBefore = getETokenAllowanceHarness(otherUser, onBahalfOf); //i: otherUser => onBahalfOf
        uint256 allowanceOtherUserForFromBefore = getETokenAllowanceHarness(otherUser, from); //i: otherUser => from
        uint256 allowanceFromForOnBehalfOfBefore = getETokenAllowanceHarness(from, onBahalfOf); //i: from => onBahalfOf 
        uint256 allowanceFromForOtherUserBefore = getETokenAllowanceHarness(from, otherUser); //i: from => otherUser
        uint256 allowanceOnBehalfOfForOtherUserBefore = getETokenAllowanceHarness(onBahalfOf, otherUser); //i: onBahalfOf => otherUser
        uint256 allowanceOnBahalfOfForFromBefore = getETokenAllowanceHarness(onBahalfOf, from); //i: onBahalfOf => from

        //FUNCTION CALL
        bool returnValueCall= transferFromMax(e, from, to);

        //VALUES AFTER
        //shares after
        Type.Shares sharesFromAfter = getUserBalanceHarness(from);
        Type.Shares sharesToAfter = getUserBalanceHarness(to);
        Type.Shares sharesotherUserAfter = getUserBalanceHarness(otherUser);

        //allowance after
        uint256 allowanceOtherUserForOnBehalfOfAfter = getETokenAllowanceHarness(otherUser, onBahalfOf); //i: otherUser => onBahalfOf
        uint256 allowanceOtherUserForFromAfter = getETokenAllowanceHarness(otherUser, from); //i: otherUser => from
        uint256 allowanceFromForOnBehalfOfAfter = getETokenAllowanceHarness(from, onBahalfOf); //i: from => onBahalfOf
        uint256 allowanceFromForOtherUserAfter = getETokenAllowanceHarness(from, otherUser); //i: from => otherUser
        uint256 allowanceOnBahalfOfForOtherUserAfter = getETokenAllowanceHarness(onBahalfOf, otherUser); //i: onBahalfOf => otherUser
        uint256 allowanceOnBahalfOfForFromAfter = getETokenAllowanceHarness(onBahalfOf, from); //i: onBahalfOf => from

        //ASSERTS
        //assert1: returnValueCall should be true
        assert(returnValueCall == true, "Return value should be true");

        //assert3: shares for from should be 0
        assert(sharesFromAfter == 0, "Shares of from should be 0");

        //assert4: shares should increase for to by finalShares
        assert(sharesToBefore + finalShares == to_mathint(sharesToAfter), "Shares of to should increase by finalShares");

        //assert5: shares should not change for otherUser
        assert(sharesotherUserBefore == sharesotherUserAfter, "Shares of otherUser should not change");

        //assert6: if allowanceFromForOnBehalfOf != max_uint256, allowance should decrease by finalShares
        assert(allowanceFromForOnBehalfOfBefore != max_uint256 => allowanceFromForOnBehalfOfBefore - finalShares == to_mathint(allowanceFromForOnBehalfOfAfter), "Allowance from => onBehalfOf should decrease by finalShares");

        //assert7: if allowanceFromForOnBehalfOf = max_uint256, allowance should stay the same
        assert(allowanceFromForOnBehalfOfBefore == max_uint256 => allowanceFromForOnBehalfOfBefore == allowanceFromForOnBehalfOfAfter, "Allowance from => onBehalfOf should stay the same");

        //assert8: allowance should not change for otherUser
        assert(allowanceOtherUserForFromBefore == allowanceOtherUserForFromAfter
        && allowanceOtherUserForOnBehalfOfBefore == allowanceOtherUserForOnBehalfOfAfter,
        "Allowance otherUser => from/onBehalfOf should not change");

        //assert9: allowance should not change for onBehalfOf
        assert(allowanceOnBahalfOfForFromBefore == allowanceOnBahalfOfForFromAfter
        && allowanceOnBehalfOfForOtherUserBefore == allowanceOnBahalfOfForOtherUserAfter,
        "Allowance onBehalfOf => from/otherUser should not change");

        //assert10: allowance from => otherUser should not change
        assert(allowanceFromForOtherUserBefore == allowanceFromForOtherUserAfter, "Allowance from => otherUser should not change");
    }

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
        bool isTransferDisabled = isTransferDisabled(e);

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

        //assert6: if isTransferDisabled, then function should revert
        assert(isTransferDisabled => reverted, "isTransferDisabled: Function call should revert");
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
        bool isTransferDisabled = isTransferDisabled(e);

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

        //assert7: if isTransferDisabled, then function should revert
        assert(isTransferDisabled => reverted, "isTransferDisabled: Function call should revert");
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
        bool isTransferDisabled = isTransferDisabled(e);

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

        //assert6: if isTransferDisabled, then function should revert
        assert(isTransferDisabled => reverted, "isTransferDisabled: Function call should revert");
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
        bool isSkimDisabled = isSkimDisabled(e);

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

        //assert6: if isSkimDisabled, then function should revert
        assert(isSkimDisabled => lastReverted, "isSkimDisabled: Function call should revert");
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
        bool isMintDisabled = isMintDisabled(e);

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

        //assert5: if isMintDisabled, then function should revert
        assert(isMintDisabled => reverted, "isMintDisabled: Function call should revert");
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
        bool isDepositDisabled = isDepositDisabled(e);

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

        //assert5: if isDepositDisabled, then function should revert
        assert(isDepositDisabled => reverted, "isDepositDisabled: Function call should revert");
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





