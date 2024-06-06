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






//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------
   
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




