import "./Base.spec";
import "./GhostPow.spec";
import "./LoadVaultSummaries.spec";
import "./Base/vault.spec";

using VaultHarness as Vault;
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;


// used to test running time
use builtin rule sanity;



//------------------------------- RULES TEST START ----------------------------------


    //deposit works
    rule depositWorks(env e){
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;
        require(receiver != currentContract);
        address onBehalfOf = actualCaller(e);
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
        // //assert1: balanceOf other user does not change
        // assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of other user should not change");

        // //assert2: finalAssets != 0 => balanceOf onBehalfOf should decrease by finalAssetsUint
        // assert(finalAssets != 0 => balanceOnBehalfOfBefore - finalAssetsUint == to_mathint(balanceOnBehalfOfAfter), "Balance of onBehalfOf should decrease by finalAssetsUint");

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

        //assert9: return value is sharesUint if finalAssets is not 0
        assert(finalAssets != 0 => returnValueCall == sharesUint, "Return value should be sharesUint if finalAssets is not 0");




    }



//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------
   

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------

















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