import "./Base.spec";
import "./GhostPow.spec";
import "./LoadVaultSummaries.spec";
import "./Base/vault.spec";

using VaultHarness as Vault;
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;


// used to test running time
use builtin rule sanity;

//invariants: vaultStorage.cash should never be smaller than the balance of the vault

//------------------------------- RULES TEST START ----------------------------------
    //invariants:
    // // 1. cash should never be bigger than the balance of the vault
    // invariant cashShouldNeverBeBiggerThanBalance(env e) 
    // Vault.vaultStorage.cash <= userAssets(e, currentContract);




//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

    //only change snapshot //@audit snapshot is not changed at all (tested by removing the code) but passes
    rule onlyChangeSnapshot(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        bool snapshotBefore = Vault.vaultStorage.snapshotInitialized;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        bool snapshotAfter = Vault.vaultStorage.snapshotInitialized;

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(snapshotBefore != snapshotAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:skim(uint256,address).selector ||
        f.selector == sig:transfer(address,uint256).selector ||
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:transferFromMax(address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the user shares");
    }

    //only change allowance
    rule onlyChangeAllowance(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //FUNCTION PARAMETER
        address user1;
        address user2;
        //VALUES BEFORE
        uint256 allowanceBefore = shareAllowanceGhost[user1][user2];

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        uint256 allowanceAfter = shareAllowanceGhost[user1][user2];

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(allowanceBefore != allowanceAfter =>
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:transferFromMax(address,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:transfer(address,uint256).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector ||
        f.selector == sig:approve(address,uint256).selector,
        "This function should not be able to change the user shares");
    }

    //only change total shares
    rule onlyChangeTotalShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        mathint totalSharesBefore = totalSharesGhost;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        mathint totalSharesAfter = totalSharesGhost;

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(totalSharesBefore != totalSharesAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:skim(uint256,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the user shares");
    }

   //only change vaultstorage.cash
    rule onlyChangeVaultCash(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //VALUES BEFORE
        Type.Assets cashBefore = Vault.vaultStorage.cash;

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Assets cashAfter = Vault.vaultStorage.cash;

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(cashBefore != cashAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:skim(uint256,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the user shares");
    }

    //only change vault shares
    rule onlyChangeUserShares(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //FUNCTION PARAMETER
        address user;
        //VALUES BEFORE
        Type.Shares sharesUserBefore = shareBalanceGhost[user];

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        Type.Shares sharesUserAfter = shareBalanceGhost[user];

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(sharesUserBefore != sharesUserAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:skim(uint256,address).selector ||
        f.selector == sig:transfer(address,uint256).selector ||
        f.selector == sig:transferFrom(address,address,uint256).selector ||
        f.selector == sig:transferFromMax(address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "This function should not be able to change the user shares");
    }

    //only change balance of collateral
    rule onlyChangeBalanceOfCollateral(env e, method f, calldataarg args) filtered{ f -> !BASE_HARNESS_FUNCTIONS(f) && !f.isView  && !f.isPure 
    } {
        //FUNCTION PARAMETER
        address user;
        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        //Balances before
        uint256 balanceUserBefore = VaultAsset.balanceOf(e,user);

        //FUNCTION CALL
        f(e, args);

        //VALUES AFTER
        //Balances after
        uint256 balanceUserAfter = VaultAsset.balanceOf(e,user);

        //ASSERTS
        // Only spesifc functions should change the balance of the collateral
        assert(balanceUserBefore != balanceUserAfter =>
        f.selector == sig:deposit(uint256,address).selector ||
        f.selector == sig:mint(uint256,address).selector ||
        f.selector == sig:redeem(uint256,address,address).selector ||
        f.selector == sig:withdraw(uint256,address,address).selector,
        "Only deposit, mint, redeem and withdraw should change the balance of the collateral");
    }

    //redeem works allowances
    rule redeemWorksAllowances(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        require(amount <= max_uint112);
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address receiver;
        address owner;
        address otherUser;
        address onBehalfOf = actualCaller(e);
        require(otherUser != owner && otherUser != onBehalfOf);
        require(onBehalfOf != owner);

        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        //Balances shares before
        Type.Shares sharesOwnerBefore = shareBalanceGhost[owner]; 
        //Allownace before
        uint256 allowanceOnBehalfForOwnerBefore = shareAllowanceGhost[owner][onBehalfOf]; //i: owner => onBehalfOf
        uint256 allowanceOnBehalfOfForOtherUserBefore = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOwnerBefore = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOtherUserForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserBefore = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner


        //FINAL VALUES
        Type.Shares finalShares = amount == max_uint256 ? sharesOwnerBefore : amountInShares;
        // Type.Assets finalAssets = sharesToAssetsDownHarness(finalShares, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = redeem(e, amount, receiver, owner);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Allownace after
        uint256 allowanceOnBehalfForOwnerAfter = shareAllowanceGhost[owner][onBehalfOf]; //i: ownder => onBehalfOf
        uint256 allowanceOtherUserForOwnerAfter = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOnBehalfOfForOtherUserAfter = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserAfter = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner

        //ASSERTS
        //assert1: if finalShares != 0 && onBehalfOf != owner && allowanceBefore != max_uint256 => allowance ownder => onBehalfOf should decrease by finalShares
        assert(finalShares != 0 && onBehalfOf != owner && allowanceOnBehalfForOwnerBefore != max_uint256 => allowanceOnBehalfForOwnerBefore - finalShares == to_mathint(allowanceOnBehalfForOwnerAfter), "Allowance owner => onBehalfOf should decrease by finalShares");

        //assert2: if allowanceBefore = max_uint256, allowance should stay the same
        assert(allowanceOnBehalfForOwnerBefore == max_uint256 => allowanceOnBehalfForOwnerBefore == allowanceOnBehalfForOwnerAfter, "Allowance owner => onBehalfOf should stay the same");

        //assert3: allowance owner => otherUser should not change
        assert(allowanceOtherUserForOwnerBefore == allowanceOtherUserForOwnerAfter, "Allowance owner => otherUser should not change");

        //assert4: allowance otherUser => onBehalfe should not change 
        assert(allowanceOtherUserForOnBehalfOfBefore == allowanceOtherUserForOnBehalfOfAfter, "Allowance otherUser => onBehalfOf should not change");

        //assert5: allowance otherUser => owner should not change
        assert(allowanceOwnerForOtherUserBefore == allowanceOwnerForOtherUserAfter, "Allowance otherUser => owner should not change");

        //assert6: allowance onBehalfOf => otherUser should not change
        assert(allowanceOnBehalfOfForOtherUserBefore == allowanceOnBehalfOfForOtherUserAfter, "Allowance onBehalfOf => otherUser should not change");

        //assert7: allowance onBehalfOf => owner should not change
        assert(allowanceOwnerForOnBehalfOfBefore == allowanceOwnerForOnBehalfOfAfter, "Allowance owner => onBehalfOf should not change");
    }

    //redeem works
    rule redeemWorks(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        require(amount <= max_uint112);
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address receiver;
        require(receiver != currentContract);
        address owner;
        address otherUser;
        require(otherUser != receiver && otherUser != owner && otherUser != currentContract);
        address onBehalfOf = actualCaller(e);

        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);

        //Balances shares before
        Type.Assets cashBefore = vaultCacheBefore.cash;
        mathint totalSharesBefore = totalSharesGhost;
        Type.Shares sharesOwnerBefore = shareBalanceGhost[owner]; //i: to fix issue with mathint, is the same value as shareBalanceGhost[owner]
        // Type.Shares sharesOwnerAsSharesBefore = uintToSharesHarness(sharesOwnerBefore);
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        //Balances collateral before
        uint256 balanceReceiverBefore = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);

        //FINAL VALUES
        Type.Shares finalShares = amount == max_uint256 ? sharesOwnerBefore : amountInShares;
        Type.Assets finalAssets = sharesToAssetsDownHarness(finalShares, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = redeem(e, amount, receiver, owner);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances shares after
        mathint totalSharesAfter = totalSharesGhost;
        mathint sharesOwnerAfter = shareBalanceGhost[owner];
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];
        //Balances collateral after
        uint256 balanceReceiverAfter = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e,currentContract);

        //ASSERTS
        //assert1: if amount = 0, the returnValueCall should be 0
        assert(amount == 0 => returnValueCall == 0, "Return value should be 0 if amount is 0");

        //assert2: if finalShares != 0, sharesOwner should decrease by finalShares
        assert(finalShares != 0 => sharesOwnerBefore - finalShares == to_mathint(sharesOwnerAfter), "Shares of owner should decrease by finalShares");

        //assert3: if finalShares != 0, totalShares should decrease by finalShares
        assert(finalShares != 0 => totalSharesBefore - finalShares == to_mathint(totalSharesAfter), "Total shares should decrease by finalShares");

        //assert4: sharesOtherUser should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should not change");

        //assert5: if finalShares != 0, balanceOf receiver should increase by finalAssets
        assert(finalShares != 0 => balanceReceiverBefore + finalAssets == to_mathint(balanceReceiverAfter), "Balance of receiver should increase by amount");

        //assert6: balanceOf otherUser should stay the same
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should stay the same");

        //assert7: if finalShares != 0, balanceOf currentContract should decrease by finalAssets
        assert(finalShares != 0 => balanceVaultBefore - finalAssets == to_mathint(balanceVaultAfter), "Balance of currentContract should decrease by amount");

        //assert8: if finalShares != 0, cash of vault should decrease by finalAssets
        assert(finalShares != 0 => vaultCacheBefore.cash - finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should decrease by finalAssets");
    }

        //withdraw works allowances
    rule withdrawWorksAllowancesAssert2To7(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        require(amount <= max_uint112);
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address receiver;
        address owner;
        address otherUser;
        address onBehalfOf = actualCaller(e);
        require(otherUser != owner && otherUser != onBehalfOf);
        require(onBehalfOf != owner);

        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        //Balances shares before
        Type.Shares sharesOwnerBefore = shareBalanceGhost[owner]; 
        //Allownace before
        uint256 allowanceOnBehalfForOwnerBefore = shareAllowanceGhost[owner][onBehalfOf]; //i: owner => onBehalfOf
        uint256 allowanceOnBehalfOfForOtherUserBefore = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOwnerBefore = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOtherUserForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserBefore = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner

        //FINAL VALUES
        Type.Assets finalAssets = uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesUpHarness(finalAssets, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = withdraw(e, amount, receiver, owner);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Allownace after
        uint256 allowanceOnBehalfForOwnerAfter = shareAllowanceGhost[owner][onBehalfOf]; //i: ownder => onBehalfOf
        uint256 allowanceOtherUserForOwnerAfter = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOnBehalfOfForOtherUserAfter = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserAfter = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner

        //ASSERTS
        //assert2: if allowanceBefore = max_uint256, allowance should stay the same
        assert(allowanceOnBehalfForOwnerBefore == max_uint256 => allowanceOnBehalfForOwnerBefore == allowanceOnBehalfForOwnerAfter, "Allowance owner => onBehalfOf should stay the same");

        //assert3: allowance owner => otherUser should not change
        assert(allowanceOtherUserForOwnerBefore == allowanceOtherUserForOwnerAfter, "Allowance owner => otherUser should not change");

        //assert4: allowance otherUser => onBehalfe should not change 
        assert(allowanceOtherUserForOnBehalfOfBefore == allowanceOtherUserForOnBehalfOfAfter, "Allowance otherUser => onBehalfOf should not change");

        //assert5: allowance otherUser => owner should not change
        assert(allowanceOwnerForOtherUserBefore == allowanceOwnerForOtherUserAfter, "Allowance otherUser => owner should not change");

        //assert6: allowance onBehalfOf => otherUser should not change
        assert(allowanceOnBehalfOfForOtherUserBefore == allowanceOnBehalfOfForOtherUserAfter, "Allowance onBehalfOf => otherUser should not change");

        //assert7: allowance onBehalfOf => owner should not change
        assert(allowanceOwnerForOnBehalfOfBefore == allowanceOwnerForOnBehalfOfAfter, "Allowance owner => onBehalfOf should not change");
    }

     //withdraw works allowances
    rule withdrawWorksAllowancesAssert1(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        require(amount <= max_uint112);
        Type.Shares amountInShares = uintToSharesHarness(amount);
        address receiver;
        address owner;
        address otherUser;
        address onBehalfOf = actualCaller(e);
        require(otherUser != owner && otherUser != onBehalfOf);
        require(onBehalfOf != owner);

        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        //Balances shares before
        Type.Shares sharesOwnerBefore = shareBalanceGhost[owner]; 
        //Allownace before
        uint256 allowanceOnBehalfForOwnerBefore = shareAllowanceGhost[owner][onBehalfOf]; //i: owner => onBehalfOf
        uint256 allowanceOnBehalfOfForOtherUserBefore = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOwnerBefore = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOtherUserForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfBefore = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserBefore = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner

        //FINAL VALUES
        Type.Assets finalAssets = uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesUpHarness(finalAssets, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = withdraw(e, amount, receiver, owner);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Allownace after
        uint256 allowanceOnBehalfForOwnerAfter = shareAllowanceGhost[owner][onBehalfOf]; //i: ownder => onBehalfOf
        uint256 allowanceOtherUserForOwnerAfter = shareAllowanceGhost[owner][otherUser]; //i: owner => otherUser
        uint256 allowanceOnBehalfOfForOtherUserAfter = shareAllowanceGhost[otherUser][onBehalfOf]; //i: otherUser => onBehalfOf
        uint256 allowanceOtherUserForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][otherUser]; //i: onBehalfOf => otherUser
        uint256 allowanceOwnerForOnBehalfOfAfter = shareAllowanceGhost[onBehalfOf][owner]; //i: onBehalfOf => owner
        uint256 allowanceOwnerForOtherUserAfter = shareAllowanceGhost[otherUser][owner]; //i: otherUser => owner

        //ASSERTS
        //assert1: if finalShares != 0 && onBehalfOf != owner && allowanceBefore != max_uint256 => allowance ownder => onBehalfOf should decrease by finalShares
        assert(finalAssets != 0 && onBehalfOf != owner && allowanceOnBehalfForOwnerBefore != max_uint256 => allowanceOnBehalfForOwnerBefore - finalShares == to_mathint(allowanceOnBehalfForOwnerAfter), "Allowance owner => onBehalfOf should decrease by finalShares");
    }

    //withdraw works
    rule withdrawWorks(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        require(receiver != currentContract);
        address owner;
        address otherUser;
        require(otherUser != receiver && otherUser != owner && otherUser != currentContract);
        address onBehalfOf = actualCaller(e);

        //VALUES BEFORE
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        //Balances shares before
        Type.Assets cashBefore = vaultCacheBefore.cash;
        mathint totalSharesBefore = totalSharesGhost;
        mathint sharesOwnerBefore = shareBalanceGhost[owner];
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        //Balances collateral before
        uint256 balanceReceiverBefore = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);

        //FINAL VALUES
        Type.Assets finalAssets = uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesUpHarness(finalAssets, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = withdraw(e, amount, receiver, owner);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances shares after
        mathint totalSharesAfter = totalSharesGhost;
        mathint sharesOwnerAfter = shareBalanceGhost[owner];
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];
        //Balances collateral after
        uint256 balanceReceiverAfter = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e,currentContract);

        //ASSERTS
        //assert1: if amount = 0, the returnValueCall should be 0
        assert(amount == 0 => returnValueCall == 0, "Return value should be 0 if amount is 0");

        //assert2: if finalAssets != 0, sharesOwner should decrease by finalShares
        assert(finalAssets != 0 => sharesOwnerBefore - finalShares == to_mathint(sharesOwnerAfter), "Shares of owner should decrease by finalShares");

        //assert3: if finalAssets != 0, totalShares should decrease by finalShares
        assert(finalAssets != 0 => totalSharesBefore - finalShares == to_mathint(totalSharesAfter), "Total shares should decrease by finalShares");

        //assert4: sharesOtherUser should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should not change");

        //assert5: if finalAssets != 0, balanceOf receiver should increase by finalAssets
        assert(finalAssets != 0 => balanceReceiverBefore + amount == to_mathint(balanceReceiverAfter), "Balance of receiver should increase by amount");

        //assert6: balanceOf otherUser should stay the same
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should stay the same");

        //assert7: if finalAssets != 0, balanceOf currentContract should decrease by finalAssets
        assert(finalAssets != 0 => balanceVaultBefore - amount == to_mathint(balanceVaultAfter), "Balance of currentContract should decrease by amount");

        //assert8: if finalAssets != 0, cash of vault should decrease by finalAssets
        assert(finalAssets != 0 => vaultCacheBefore.cash - finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should decrease by finalAssets");
    }

    //skim works
    rule skimWorks1(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address otherUser;
        require(otherUser != receiver);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        Type.Assets cashBefore = vaultCacheBefore.cash;

        //VALUES BEFORE
        mathint totalSharesBefore = totalSharesGhost;
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        //Balances before
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceReceiverBefore = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        Type.Assets assetsAvailable = to_mathint(balanceVaultBefore) <= to_mathint(vaultCacheBefore.cash) ? 0 : uintToAssetsHarness(require_uint256(balanceVaultBefore - vaultCacheBefore.cash));

        //FINAL VALUES
        Type.Assets finalAssets = amount == max_uint256 ? assetsAvailable : uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = skim(e, amount, receiver);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances after
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceReceiverAfter = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        mathint totalSharesAfter = totalSharesGhost;
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];

        //ASSERTS
        //assert1: collateralBalance of currentContract should stay the same
        assert(balanceVaultBefore == balanceVaultAfter, "Balance of currentContract should stay the same");

        //assert2: Balance of receiver should stay the same
        assert(balanceReceiverBefore == balanceReceiverAfter, "Balance of receiver should stay the same");

        //assert3: Balance of otherUser should stay the same
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of otherUser should stay the same");

        //assert4: if finalAssets = 0, the returnValueCall should be 0
        assert(finalAssets == 0 => returnValueCall == 0, "Return value should be 0 if finalAssets is 0");
    }

    //skim works
    rule skimWorks2(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        address otherUser;
        require(otherUser != receiver);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset);
        Type.Assets cashBefore = vaultCacheBefore.cash;

        //VALUES BEFORE
        mathint totalSharesBefore = totalSharesGhost;
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        //Balances before
        uint256 balanceVaultBefore = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceReceiverBefore = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        Type.Assets assetsAvailable = to_mathint(balanceVaultBefore) <= to_mathint(vaultCacheBefore.cash) ? 0 : uintToAssetsHarness(require_uint256(balanceVaultBefore - vaultCacheBefore.cash));

        //FINAL VALUES
        Type.Assets finalAssets = amount == max_uint256 ? assetsAvailable : uintToAssetsHarness(amount);
        Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCacheBefore);

        //FUNCTION CALL
        uint256 returnValueCall = skim(e, amount, receiver);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances after
        uint256 balanceVaultAfter = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceReceiverAfter = VaultAsset.balanceOf(e,receiver);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        mathint totalSharesAfter = totalSharesGhost;
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];

        //ASSERTS
        //assert5: finalAssets !=0 => vaultChash should be increased by finalAssets
        assert(finalAssets != 0 => vaultCacheBefore.cash + finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should increase by finalAssets");

        //assert6: finalAssets !=0 => totalShares should increase by finalShares
        assert(finalAssets != 0 => totalSharesBefore + finalShares == to_mathint(totalSharesAfter), "Total shares should increase by finalShares");

        //assert7: finalAssets !=0 => receiverShares should be increased by finalShares
        assert(finalAssets != 0 => sharesReceiverBefore + finalShares == to_mathint(sharesReceiverAfter), "Shares of receiver should increase by finalShares");

        //assert8: otherUserShares should stay the same
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should stay the same");
    }
    
    //deposit works
    rule depositWorks(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        require(receiver != currentContract);
        address onBehalfOf = actualCaller(e);
        require(onBehalfOf != currentContract);
        address otherUser;
        require(otherUser != receiver && otherUser != currentContract && otherUser != onBehalfOf);
        uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e,onBehalfOf);

        Type.Assets finalAssets = 
        amount == max_uint256 ? 
        uintToAssetsHarness(balanceOnBehalfOfBefore) : uintToAssetsHarness(amount);
        uint256 finalAssetsUint = assetsToUintHarness(finalAssets);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        Type.Shares finalShares = assetsToSharesDownHarness(finalAssets, vaultCacheBefore);
        uint256 sharesUint = sharesToUintHarness(finalShares);

        //VALUES BEFORE
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset); 

        //Balances before
        uint256 balanceCurrentContractBefore = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint totalSharesBefore = totalSharesGhost;

        //FUNCTION CALL
        uint256 returnValueCall = deposit(e, amount, receiver);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances after
        uint256 balanceOnBehalfOfAfter = VaultAsset.balanceOf(e,onBehalfOf);
        uint256 balanceCurrentContractAfter = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint totalSharesAfter = totalSharesGhost;

        //ASSERTS
        //assert1: balanceOf other user does not change
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should not change");

        //assert2: finalAssets != 0 => balanceOf onBehalfOf should decrease by finalAssetsUint
        assert(finalAssets != 0 => balanceOnBehalfOfBefore - finalAssetsUint == to_mathint(balanceOnBehalfOfAfter), "Balance of onBehalfOf should decrease by finalAssetsUint");

        //assert3: finalAssets != 0 => balance of currentContract should increase by finalAssetsUint
        assert(finalAssets != 0 => balanceCurrentContractBefore + finalAssetsUint == to_mathint(balanceCurrentContractAfter), "Balance of currentContract should increase by finalAssetsUint");

        //assert4: finalAssets != 0 => cash of vault should increase by finalAssets
        assert(finalAssets != 0 => vaultCacheBefore.cash + finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should increase by finalAssets");

        //assert5: share of other user should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should not change");

        //assert6: finalAssets != 0 =>share of receiver should increase by finalShares
        assert(finalAssets != 0 => sharesReceiverBefore + finalShares == sharesReceiverAfter, "Shares of receiver should increase by finalShares");

        //assert7: finalAssets != 0 => totalShares should increase by finalShares
        assert(finalAssets != 0 => totalSharesBefore + finalShares == totalSharesAfter, "Total shares should increase by finalShares");

        //assert8: return value is 0 if finalAssets is 0
        assert(finalAssets == 0 => returnValueCall == 0, "Return value should be 0 if finalAssets is 0");

        // //assert9: return value is sharesUint if finalAssets is not 0 //@audit times out on its own
        // assert(finalAssets != 0 => returnValueCall == sharesUint, "Return value should be sharesUint if finalAssets is not 0");
    }

    //mint works
    rule mintWorks(env e){
        //FUNCTION PARAMETER
        uint256 amount; //i: shares to be minted
        address receiver;
        require(receiver != currentContract);
        address onBehalfOf = actualCaller(e);
        require(onBehalfOf != currentContract);
        address otherUser;
        require(otherUser != receiver && otherUser != currentContract && otherUser != onBehalfOf);
        uint256 balanceOnBehalfOfBefore = VaultAsset.balanceOf(e,onBehalfOf);
        Type.VaultCache vaultCacheBefore = getCurrentVaultCacheHarness();
        //final Values
        Type.Shares finalShares = uintToSharesHarness(amount);
        Type.Assets finalAssets = shareToAssetsUpHarness(finalShares, vaultCacheBefore);
        uint256 finalAssetsUint = assetsToUintHarness(finalAssets);

        //VALUES BEFORE
        address collateral = vaultCacheBefore.asset;
        require(collateral == VaultAsset); 

        //Balances before
        uint256 balanceCurrentContractBefore = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceOtherUserBefore = VaultAsset.balanceOf(e,otherUser);
        mathint sharesOtherUserBefore = shareBalanceGhost[otherUser];
        mathint sharesReceiverBefore = shareBalanceGhost[receiver];
        mathint totalSharesBefore = totalSharesGhost;

        //FUNCTION CALL
        uint256 returnValueCall = mint(e, amount, receiver);

        //VALUES AFTER
        Type.VaultCache vaultCacheAfter = getCurrentVaultCacheHarness();
        //Balances after
        uint256 balanceOnBehalfOfAfter = VaultAsset.balanceOf(e,onBehalfOf);
        uint256 balanceCurrentContractAfter = VaultAsset.balanceOf(e,currentContract);
        uint256 balanceOtherUserAfter = VaultAsset.balanceOf(e,otherUser);
        mathint sharesOtherUserAfter = shareBalanceGhost[otherUser];
        mathint sharesReceiverAfter = shareBalanceGhost[receiver];
        mathint totalSharesAfter = totalSharesGhost;

        //ASSERTS
        //assert1: balanceOf other user does not change
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should not change");

        //assert2: finalShares != 0 => balanceOf onBehalfOf should decrease by finalAssetsUint
        assert(finalShares != 0 => balanceOnBehalfOfBefore - finalAssetsUint == to_mathint(balanceOnBehalfOfAfter), "Balance of onBehalfOf should decrease by finalAssetsUint");

        //assert3: finalShares != 0 => balance of currentContract should increase by finalAssetsUint
        assert(finalShares != 0 => balanceCurrentContractBefore + finalAssetsUint == to_mathint(balanceCurrentContractAfter), "Balance of currentContract should increase by finalAssetsUint");

        //assert4: finalShares != 0 => cash of vault should increase by finalAssets
        assert(finalShares != 0 => vaultCacheBefore.cash + finalAssets == to_mathint(vaultCacheAfter.cash), "Cash of vault should increase by finalAssets");

        //assert5: share of other user should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares of other user should not change");

        //assert6: finalShares != 0 =>share of receiver should increase by finalShares
        assert(finalShares != 0 => sharesReceiverBefore + finalShares == sharesReceiverAfter, "Shares of receiver should increase by finalShares");

        //assert7: finalShares != 0 => totalShares should increase by finalShares
        assert(finalShares != 0 => totalSharesBefore + finalShares == totalSharesAfter, "Total shares should increase by finalShares");

        //assert8: return value is 0 if finalShares is 0
        assert(finalShares == 0 => returnValueCall == 0, "Return value should be 0 if finalAssets is 0");

        // //assert9: return value is sharesUint if finalAssets is not 0 //@audit times out on its own
        // assert(finalAssets != 0 => returnValueCall == sharesUint, "Return value should be sharesUint if finalAssets is not 0");
    }

    //transfer works
    rule transferWorks(env e){
        //FUNCTION PARAMETER
        address to;
        uint256 amount;
        address otherUser1;
        address otherUser2;
        Type.Shares finalShares = uintToSharesHarness(amount);
        address from = actualCaller(e); //i: onBahalfOf  address
        require(otherUser1 != to && otherUser1 != from);
        require(from != to);

        //VALUES BEFORE
        //shares before
        Type.Shares sharesFromBefore = shareBalanceGhost[from];
        Type.Shares sharesToBefore = shareBalanceGhost[to];
        Type.Shares sharesOtherUser1Before = shareBalanceGhost[otherUser1];

        //allowance before
        uint256 allowanceOtherUser1ForOtherUser2 = shareAllowanceGhost[otherUser1][otherUser2]; //i: otherUser1 => otherUser2 covers any change in allowance 

        //FUNCTION CALL
        bool returnValueCall= transfer(e, to, amount);

        //VALUES AFTER
        //shares after
        Type.Shares sharesFromAfter = shareBalanceGhost[from];
        Type.Shares sharesToAfter = shareBalanceGhost[to];
        Type.Shares sharesOtherUser1After = shareBalanceGhost[otherUser1];

        //allowance after
        uint256 allowanceOtherUser1ForOtherUser2After = shareAllowanceGhost[otherUser1][otherUser2]; //i: otherUser1 => otherUser2 covers any change in allowance

        //ASSERTS
        //assert1: returnValueCall should be true
        assert(returnValueCall == true, "Return value should be true");

        //assert2: allowance should not change
        assert(allowanceOtherUser1ForOtherUser2 == allowanceOtherUser1ForOtherUser2After, "Allowance should not change");

        //assert3: shares should decrease for from by finalShares
        assert(sharesFromBefore - finalShares == to_mathint(sharesFromAfter), "Shares of from should decrease by finalShares");

        //assert4: shares should increase for to by finalShares
        assert(sharesToBefore + finalShares == to_mathint(sharesToAfter), "Shares of to should increase by finalShares");

        //assert5: shares should not change for otherUser1
        assert(sharesOtherUser1Before == sharesOtherUser1After, "Shares of otherUser1 should not change");
    } 

    //transferFrom works
    rule transferFromWorks(env e){
        //FUNCTION PARAMETER
        address from;
        address to;
        uint256 amount;
        address otherUser;
        Type.Shares finalShares = uintToSharesHarness(amount);
        address onBahalfOf = actualCaller(e); //i: onBahalfOf  address
        require(otherUser != from && otherUser != onBahalfOf && otherUser != to);
        require(from != to && from != onBahalfOf);

        //VALUES BEFORE
        //shares before
        Type.Shares sharesFromBefore = shareBalanceGhost[from];
        Type.Shares sharesToBefore = shareBalanceGhost[to];
        Type.Shares sharesotherUserBefore = shareBalanceGhost[otherUser];

        //allowance before
        uint256 allowanceotherUserForOnBehalfOfBefore = shareAllowanceGhost[otherUser][onBahalfOf]; //i: otherUser => onBahalfOf
        uint256 allowanceotherUserForFromBefore = shareAllowanceGhost[otherUser][from]; //i: otherUser => from
        uint256 allowanceFromForOnBehalfOfBefore = shareAllowanceGhost[from][onBahalfOf]; //i: from => onBahalfOf 
        uint256 allowanceFromForotherUserBefore = shareAllowanceGhost[from][otherUser]; //i: from => otherUser
        uint256 allowanceOnBehalfOfForotherUserBefore = shareAllowanceGhost[onBahalfOf][otherUser]; //i: onBahalfOf => otherUser
        uint256 allowanceOnBahalfOfForFromBefore = shareAllowanceGhost[onBahalfOf][from]; //i: onBahalfOf => from

        //FUNCTION CALL
        bool returnValueCall= transferFrom(e, from, to, amount);

        //VALUES AFTER
        //shares after
        Type.Shares sharesFromAfter = shareBalanceGhost[from];
        Type.Shares sharesToAfter = shareBalanceGhost[to];
        Type.Shares sharesotherUserAfter = shareBalanceGhost[otherUser];

        //allowance after
        uint256 allowanceotherUserForOnBehalfOfAfter = shareAllowanceGhost[otherUser][onBahalfOf]; //i: otherUser => onBahalfOf
        uint256 allowanceotherUserForFromAfter = shareAllowanceGhost[otherUser][from]; //i: otherUser => from
        uint256 allowanceFromForOnBehalfOfAfter = shareAllowanceGhost[from][onBahalfOf]; //i: from => onBahalfOf
        uint256 allowanceFromForotherUserAfter = shareAllowanceGhost[from][otherUser]; //i: from => otherUser
        uint256 allowanceOnBahalfOfForotherUserAfter = shareAllowanceGhost[onBahalfOf][otherUser]; //i: onBahalfOf => otherUser
        uint256 allowanceOnBahalfOfForFromAfter = shareAllowanceGhost[onBahalfOf][from]; //i: onBahalfOf => from
    
        //ASSERTS
        //assert1: returnValueCall should be true
        assert(returnValueCall == true, "Return value should be true");

        //assert3: shares should decrease for from by finalShares
        assert(sharesFromBefore - finalShares == to_mathint(sharesFromAfter), "Shares of from should decrease by finalShares");

        //assert4: shares should increase for to by finalShares
        assert(sharesToBefore + finalShares == to_mathint(sharesToAfter), "Shares of to should increase by finalShares");

        //assert5: shares should not change for otherUser
        assert(sharesotherUserBefore == sharesotherUserAfter, "Shares of otherUser should not change");

        //assert6: if allowanceFromForOnBehalfOf != max_uint256, allowance should decrease by finalShares
        assert(allowanceFromForOnBehalfOfBefore != max_uint256 => allowanceFromForOnBehalfOfBefore - finalShares == to_mathint(allowanceFromForOnBehalfOfAfter), "Allowance from => onBehalfOf should decrease by finalShares");

        //assert7: if allowanceFromForOnBehalfOf = max_uint256, allowance should stay the same
        assert(allowanceFromForOnBehalfOfBefore == max_uint256 => allowanceFromForOnBehalfOfBefore == allowanceFromForOnBehalfOfAfter, "Allowance from => onBehalfOf should stay the same");

        //assert8: allowance should not change for otherUser
        assert(allowanceotherUserForFromBefore == allowanceotherUserForFromAfter
        && allowanceotherUserForOnBehalfOfBefore == allowanceotherUserForOnBehalfOfAfter,
        "Allowance otherUser => from/onBehalfOf should not change");

        //assert9: allowance should not change for onBehalfOf
        assert(allowanceOnBahalfOfForFromBefore == allowanceOnBahalfOfForFromAfter
        && allowanceOnBehalfOfForotherUserBefore == allowanceOnBahalfOfForotherUserAfter,
        "Allowance onBehalfOf => from/otherUser should not change");

        //assert10: allowance from => otherUser should not change
        assert(allowanceFromForotherUserBefore == allowanceFromForotherUserAfter, "Allowance from => otherUser should not change");
    } 

//------------------------------- RULES OK END ------------------------------------



//----------------------OLD RULES START-------------------------

    ////////////////////////////////////////////////////////////////////////////////
    ////           #  asset To shares mathematical properties                  /////
    ////////////////////////////////////////////////////////////////////////////////

    rule conversionOfZero {
        env e;
        uint256 convertZeroShares = convertToAssets(e, 0);
        uint256 convertZeroAssets = convertToShares(e, 0);

        assert convertZeroShares == 0,
            "converting zero shares must return zero assets";
        assert convertZeroAssets == 0,
            "converting zero assets must return zero shares";
    }


    rule convertToAssetsWeakAdditivity() {
        env e;
        uint256 sharesA; uint256 sharesB;
        require sharesA + sharesB < max_uint128
            && convertToAssets(e, sharesA) + convertToAssets(e, sharesB) < to_mathint(max_uint256)
            && convertToAssets(e, require_uint256(sharesA + sharesB)) < max_uint256;
        assert convertToAssets(e, sharesA) + convertToAssets(e, sharesB) <= to_mathint(convertToAssets(e, require_uint256(sharesA + sharesB))),
            "converting sharesA and sharesB to assets then summing them must yield a smaller or equal result to summing them then converting";
    }


    rule convertToSharesWeakAdditivity() {
        env e;
        uint256 assetsA; uint256 assetsB;
        require assetsA + assetsB < max_uint128
            && convertToAssets(e, assetsA) + convertToAssets(e, assetsB) < to_mathint(max_uint256)
            && convertToAssets(e, require_uint256(assetsA + assetsB)) < max_uint256;
        assert convertToAssets(e, assetsA) + convertToAssets(e, assetsB) <= to_mathint(convertToAssets(e, require_uint256(assetsA + assetsB))),
            "converting assetsA and assetsB to shares then summing them must yield a smaller or equal result to summing them then converting";
    }


    rule conversionWeakMonotonicity {
        env e;
        uint256 smallerShares; uint256 largerShares;
        uint256 smallerAssets; uint256 largerAssets;

        assert smallerShares < largerShares => convertToAssets(e, smallerShares) <= convertToAssets(e, largerShares),
            "converting more shares must yield equal or greater assets";
        assert smallerAssets < largerAssets => convertToShares(e, smallerAssets) <= convertToShares(e, largerAssets),
            "converting more assets must yield equal or greater shares";
    }


    rule conversionWeakIntegrity() {
        env e;
        uint256 sharesOrAssets;
        assert convertToShares(e, convertToAssets(e, sharesOrAssets)) <= sharesOrAssets,
            "converting shares to assets then back to shares must return shares less than or equal to the original amount";
        assert convertToAssets(e, convertToShares(e, sharesOrAssets)) <= sharesOrAssets,
            "converting assets to shares then back to assets must return assets less than or equal to the original amount";
    }


    rule convertToCorrectness(uint256 amount, uint256 shares)
    {
        env e;
        assert amount >= convertToAssets(e, convertToShares(e, amount));
        assert shares >= convertToShares(e, convertToAssets(e, shares));
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////                   #    Unit Test                                      /////
    ////////////////////////////////////////////////////////////////////////////////


    rule zeroDepositZeroShares(uint assets, address receiver)
    {
        env e;
        
        uint shares = deposit(e,assets, receiver);
        // In this Vault, max_uint256 as an argument will transfer all assets
        // to the vault . This precondition rules out the case where
        // the depositor calls deposit with a blance of 0 in the underlying
        // asset and gives max_uint256 as the shares.
        require assets < max_uint256;

        assert shares == 0 <=> assets == 0;
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////                    #    Valid State                                   /////
    ////////////////////////////////////////////////////////////////////////////////

    invariant assetsMoreThanSupply(env e)
        totalAssets(e) >= totalSupply(e)
        {
            preserved {
                require e.msg.sender != currentContract;
                require actualCaller(e) != currentContract;
                require actualCallerCheckController(e) != currentContract;
                address any;
                safeAssumptions(e, any , actualCaller(e));
                safeAssumptions(e, any , actualCallerCheckController(e));
            }
        }


    invariant noSupplyIfNoAssets(env e)
        noSupplyIfNoAssetsDef(e)     // see defition in "helpers and miscellaneous" section
        {
            preserved {
                safeAssumptions(e, _, e.msg.sender);
            }
        }


    invariant noAssetsIfNoSupply(env e) 
        ( totalAssets(e) == 0 => ( totalSupply(e) == 0 ))

        {
            preserved {
                address any;
                safeAssumptions(e, any, actualCaller(e));
                safeAssumptions(e, any, actualCallerCheckController(e));
            }
        }


    ghost mathint sumOfBalances {
        init_state axiom sumOfBalances == 0;
    }

    hook Sstore currentContract.vaultStorage.users[KEY address addy].data VaultHarness.PackedUserSlot newValue (VaultHarness.PackedUserSlot oldValue)  {
        sumOfBalances = sumOfBalances + newValue - oldValue;
    }

    hook Sload VaultHarness.PackedUserSlot val currentContract.vaultStorage.users[KEY address addy].data  {
        require sumOfBalances >= to_mathint(val);
    }

    invariant totalSupplyIsSumOfBalances(env e)
        to_mathint(totalSupply(e)) == sumOfBalances;



    ////////////////////////////////////////////////////////////////////////////////
    ////                    #     State Transition                             /////
    ////////////////////////////////////////////////////////////////////////////////

    rule underlyingCannotChange() {
        address originalAsset = asset();

        method f; env e; calldataarg args;
        f(e, args);

        address newAsset = asset();

        assert originalAsset == newAsset,
            "the underlying asset of a contract must not change";
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////                    #   High Level                                    /////
    ////////////////////////////////////////////////////////////////////////////////

    rule dustFavorsTheHouse(uint assetsIn )
    {
        env e;
            
        require e.msg.sender != currentContract;
        safeAssumptions(e,e.msg.sender,e.msg.sender);
        uint256 totalSupplyBefore = totalSupply(e);

        // uint balanceBefore = ERC20a.balanceOf(e, currentContract);
        uint balanceBefore = currentContract.balanceOf(e, currentContract);

        uint shares = deposit(e,assetsIn, e.msg.sender);
        uint assetsOut = redeem(e,shares,e.msg.sender,e.msg.sender);

        // uint balanceAfter = ERC20a.balanceOf(e, currentContract);
        uint balanceAfter = currentContract.balanceOf(e, currentContract);
        assert balanceAfter >= balanceBefore;
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////                       #   Risk Analysis                           /////////
    ////////////////////////////////////////////////////////////////////////////////

    invariant vaultSolvency(env e)
        totalAssets(e) >= totalSupply(e)  && userAssets(e, currentContract) >= require_uint256(cache_cash(e))  {
        preserved {
                requireInvariant totalSupplyIsSumOfBalances(e);
                require e.msg.sender != currentContract;
                require actualCaller(e) != currentContract;
                require actualCallerCheckController(e) != currentContract;
                require currentContract != asset(); 
            }
        }


    rule redeemingAllValidity() { 
        env e;
        address owner; 
        uint256 shares; require shares == balanceOf(e, owner);
        
        safeAssumptions(e, _, owner);
        redeem(e, shares, _, owner);
        uint256 ownerBalanceAfter = balanceOf(e, owner);
        assert ownerBalanceAfter == 0;
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////               # stakeholder properties  (Risk Analysis )         //////////
    ////////////////////////////////////////////////////////////////////////////////

    rule reclaimingProducesAssets(method f)
    filtered {
        f -> f.selector == sig:withdraw(uint256,address,address).selector
        || f.selector == sig:redeem(uint256,address,address).selector
    }
    {
        env e; uint256 assets; uint256 shares;
        address receiver; address owner;
        require currentContract != e.msg.sender
            && currentContract != receiver
            && currentContract != owner;

        safeAssumptions(e, receiver, owner);

        uint256 ownerSharesBefore = balanceOf(e, owner);
        uint256 receiverAssetsBefore = userAssets(e, receiver);

        callReclaimingMethods(e, f, assets, shares, receiver, owner);

        uint256 ownerSharesAfter = balanceOf(e, owner);
        uint256 receiverAssetsAfter = userAssets(e, receiver);

        assert ownerSharesBefore > ownerSharesAfter <=> receiverAssetsBefore < receiverAssetsAfter,
            "an owner's shares must decrease if and only if the receiver's assets increase";
    }



    ////////////////////////////////////////////////////////////////////////////////
    ////                        # helpers and miscellaneous                //////////
    ////////////////////////////////////////////////////////////////////////////////

    definition noSupplyIfNoAssetsDef(env e) returns bool = 
        // for this ERC4626 implementation balanceOf(Vault) is not the same as total assets
        // ( userAssets(e, currentContract) == 0 => totalSupply(e) == 0 ) &&
        ( totalAssets(e) == 0 => ( totalSupply(e) == 0 ));


    function safeAssumptions(env e, address receiver, address owner) {
        require currentContract != asset(); // Although this is not disallowed, we assume the contract's underlying asset is not the contract itself
        requireInvariant totalSupplyIsSumOfBalances(e);
        requireInvariant vaultSolvency(e);
        requireInvariant noAssetsIfNoSupply(e);
        requireInvariant noSupplyIfNoAssets(e);
        requireInvariant assetsMoreThanSupply(e); 

        require ( 
            (receiver != owner 
                =>  balanceOf(e, owner) + balanceOf(e, receiver) <= to_mathint(totalSupply(e)))
                    && balanceOf(e, receiver) <= totalSupply(e)
                    && balanceOf(e, owner) <= totalSupply(e));
    }


    // A helper function to set the receiver 
    function callReceiverFunctions(method f, env e, address receiver) {
        uint256 amount;
        if (f.selector == sig:deposit(uint256,address).selector) {
            deposit(e, amount, receiver);
        } else if (f.selector == sig:mint(uint256,address).selector) {
            mint(e, amount, receiver);
        } else if (f.selector == sig:withdraw(uint256,address,address).selector) {
            address owner;
            withdraw(e, amount, receiver, owner);
        } else if (f.selector == sig:redeem(uint256,address,address).selector) {
            address owner;
            redeem(e, amount, receiver, owner);
        } else {
            calldataarg args;
            f(e, args);
        }
    }


    function callContributionMethods(env e, method f, uint256 assets, uint256 shares, address receiver) {
        if (f.selector == sig:deposit(uint256,address).selector) {
            deposit(e, assets, receiver);
        }
        if (f.selector == sig:mint(uint256,address).selector) {
            mint(e, shares, receiver);
        }
    }


    function callReclaimingMethods(env e, method f, uint256 assets, uint256 shares, address receiver, address owner) {
        if (f.selector == sig:withdraw(uint256,address,address).selector) {
            withdraw(e, assets, receiver, owner);
        }
        if (f.selector == sig:redeem(uint256,address,address).selector) {
            redeem(e, shares, receiver, owner);
        }
    }


    function callFunctionsWithReceiverAndOwner(env e, method f, uint256 assets, uint256 shares, address receiver, address owner) {
        if (f.selector == sig:withdraw(uint256,address,address).selector) {
            withdraw(e, assets, receiver, owner);
        }
        if (f.selector == sig:redeem(uint256,address,address).selector) {
            redeem(e, shares, receiver, owner);
        } 
        if (f.selector == sig:deposit(uint256,address).selector) {
            deposit(e, assets, receiver);
        }
        if (f.selector == sig:mint(uint256,address).selector) {
            mint(e, shares, receiver);
        }
        if (f.selector == sig:transferFrom(address,address,uint256).selector) {
            transferFrom(e, owner, receiver, shares);
        }
        else {
            calldataarg args;
            f(e, args);
        }
    }
//----------------------OLD RULES END----------------------------