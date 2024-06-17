import "./Base.spec";
import "./Base/borrowing_revert.spec";
using EthereumVaultConnector as EVC;
using DummyERC20A as VaultAsset;
using BorrowingHarness as BorrowingHarness;



// used to test running time
use builtin rule sanity;


//------------------------------- RULES OK START ------------------------------------



    //borrow Reverts work
    rule borrowReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        BorrowingHarness.Assets amountAsAssests = uintToAssetsHarness(e, amount);
        address receiver;
        address onBehalfOf = actualCaller(e);

        //VALUES BEFORE
        BorrowingHarness.VaultCache vaultCacheBefore = CVLUpdateVault();
        BorrowingHarness.Assets cashBefore = BorrowingHarness.vaultStorage.cash;
        BorrowingHarness.Assets targetAmountAsAssets = 
            amount == max_uint256 ? 
            cashBefore : 
            amountAsAssests;
        bool vaultIsController = vaultIsController(onBehalfOf);
        bool isNotSet = isNotSetCompatibeAssetHarness(vaultCacheBefore.configFlags);
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(receiver);
        bool opSet = isBorrowSet(e, vaultCacheBefore.hookedOps);
        address hookTarget = getHookTargetHarness();

 
        //function call
        borrow@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
         //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => reverted, "Only EVC can call pullDebt");

        //assert2: if onBehalfOf is 0, then revert
        assert(onBehalfOf == 0 => reverted, "On behalf of should not be address(0)");

        //assert3: if vault not controller, then revert
        assert(!vaultIsController => reverted, "Vault needs to be controller");

        //assert4: if assets > vaultCache.cash, then revert
        assert(targetAmountAsAssets > cashBefore => reverted, "Amount should not be greater than the vault cash");

        //assert5: if receiver is 0, then revert
        assert(amountAsAssests != 0 => receiver == 0 => reverted, "Receiver should not be address(0)");

        //assert6: if configflag is not set and isKnownNonOwnerAccount(receiver), then revert
        assert(amountAsAssests != 0 => isNotSet && isKnownNonOwnerAccount => reverted, "Config flag should be set and receiver should not be a known non owner account");

        //assert7: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

    }

 

    //pullDebt reverts  
    rule pullDebtReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address from;
        address onBehalfOf;
        bool vaultIsController;
        onBehalfOf, vaultIsController = EVC.getCurrentOnBehalfOfAccount(e, currentContract);
        BorrowingHarness.VaultCache vaultCache = CVLUpdateVault();
        BorrowingHarness.Owed fromOwedBefore;
        BorrowingHarness.Owed fromPrevOwedBefore;
        fromOwedBefore, fromPrevOwedBefore = CVLLoadUserBorrow(vaultCache, from);
        BorrowingHarness.Assets amountAsAssests = amount == max_uint256 ? owedToAssetsUpHarness(e,fromOwedBefore) : unitToAssetsHarness(e, amount);
        BorrowingHarness.Owed amountAsOwed = assetsToOwedHarness(e,amountAsAssests);
        BorrowingHarness.Owed finalAmount = finalAmountDustHarness(amountAsOwed, fromOwedBefore);

        //VALUES BEFORE
        bool opSet = isPullDebtSet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();


        //FUNCTION CALL
        pullDebt@withrevert(e, amount, from);

        //VALUES AFTER

        //ASSERTS
        //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => lastReverted, "Only EVC can call pullDebt");

        //assert2: if onBehalfOf is 0, then revert
        assert(onBehalfOf == 0 => lastReverted, "On behalf of should not be address(0)");

        //assert3: if vault not controller, then revert
        assert(!vaultIsController => lastReverted, "Vault needs to be controller");

        //assert4: if from = onBehalfOf, then revert
        assert(from == onBehalfOf => lastReverted, "From should not be the same as onBehalfOf");

        //assert5: if finalAmount > fromOwedBefore, then revert
        assert(finalAmount > fromOwedBefore => lastReverted, "Final amount should not be greater than the from owed");

        //assert6: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => lastReverted, "opSet and hookTarget is 0 => Function should revert");

    }


    //repay reverts
    rule repayReverts(env e) {
        //FUNCTION PARAMETER
        uint256 amount;
        address receiver;

        //VALUES BEFORE
        BorrowingHarness.VaultCache vaultCache = CVLUpdateVault();
        address onBehalfOf = actualCaller(e);
        BorrowingHarness.Owed owed;
        BorrowingHarness.Owed owedPrev;
        owed, owedPrev = CVLLoadUserBorrow(vaultCache, receiver);
        BorrowingHarness.Owed assets = toAssetHarness(amount == max_uint256 ? owed : amount); //i: amount to repay
        bool opSet = isRepaySet(e, vaultCache.hookedOps);
        address hookTarget = getHookTargetHarness();


        //FUNCTION CALL
        repay@withrevert(e, amount, receiver);
        bool reverted = lastReverted;

        //ASSERTS
        //assert1: if e.msg.sender is not evc, then revert
        assert(EVC != e.msg.sender => reverted, "Only EVC can call repay");

        //assert2: if onBehalfOf is address(0), then revert
        assert(onBehalfOf == 0 => reverted, "On behalf of should not be address(0)");

        //assert3: if assets > owed, then revert
        assert(to_mathint(assets) > to_mathint(owed) => reverted, "Amount should not be greater than the owed");

        //assert4: if opSet && hookTarget == 0, revert
        assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
