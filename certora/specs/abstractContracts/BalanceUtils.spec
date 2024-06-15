import "../Base/abstractBase.spec";

using BalanceUtilsHarness as BalanceUtils;

// used to test running time
use builtin rule sanity;

methods{
     function getTotalSharesHarness() external returns (Type.Shares) envfree;
     function getAllowanceHarness(address owner, address spender) external returns (uint256) envfree;
}


//------------------------------- RULES OK START ------------------------------------

    //decreaseAllowance works
    rule decreaseAllowanceWorks(env e){
        //FUNCTION PARAMETER
        address owner;
        address spender;
        address otherUser;
        require(otherUser != owner && otherUser != spender);
        Type.Shares amount;
        uint256 amountInUint = sharesToUintHarness(amount);

        //VALUES BEFORE
        uint256 allowanceOwnerSpenderBefore = getAllowanceHarness(owner, spender);
        uint256 allowanceOwnerOtherUserBefore = getAllowanceHarness(owner, otherUser);
        uint256 allowanceSpenderOwnerBefore = getAllowanceHarness(spender, owner);
        uint256 allowanceSpenderOtherUserBefore = getAllowanceHarness(spender, otherUser);
        uint256 allowanceOtherUserOwnerBefore = getAllowanceHarness(otherUser, owner);
        uint256 allowanceOtherUserSpenderBefore = getAllowanceHarness(otherUser, spender);

        //FUNCTION CALL
        decreaseAllowanceHarness@withrevert(e, owner, spender, amount);
        bool reverted = lastReverted;

        //VALUES AFTER
        uint256 allowanceOwnerSpenderAfter = getAllowanceHarness(owner, spender);
        uint256 allowanceOwnerOtherUserAfter = getAllowanceHarness(owner, otherUser);
        uint256 allowanceSpenderOwnerAfter = getAllowanceHarness(spender, owner);
        uint256 allowanceSpenderOtherUserAfter = getAllowanceHarness(spender, otherUser);
        uint256 allowanceOtherUserOwnerAfter = getAllowanceHarness(otherUser, owner);
        uint256 allowanceOtherUserSpenderAfter = getAllowanceHarness(otherUser, spender);

        //ASSERTS
        //asser1: if amount = 0, allowanceOwnerSpenderBefore = allowanceOwnerSpenderAfter
        assert(amount == 0 => allowanceOwnerSpenderBefore == allowanceOwnerSpenderAfter, "Allowance should not change");

        //asser2: if owner = spender, allowanceOwnerSpenderBefore = allowanceOwnerSpenderAfter
        assert(owner == spender => allowanceOwnerSpenderBefore == allowanceOwnerSpenderAfter, "Allowance should not change");

        //assert3: if allowanceOwnerSpenderBefore < amountInUint, revert
        assert(amount != 0 && owner != spender && allowanceOwnerSpenderBefore != max_uint256 && allowanceOwnerSpenderBefore < amountInUint => reverted, "Call should revert");

        //assert4: if !reverted => allowanceOwnerSpenderAfter = allowanceOwnerSpenderBefore - amountInUint
        assert(!reverted && amount != 0 && owner != spender && allowanceOwnerSpenderBefore != max_uint256 => to_mathint(allowanceOwnerSpenderAfter) == allowanceOwnerSpenderBefore - amountInUint, "Allowance should be decreased by amount");

        //assert5: other allowances should not change
        assert(allowanceOwnerOtherUserBefore == allowanceOwnerOtherUserAfter &&
        allowanceSpenderOwnerBefore == allowanceSpenderOwnerAfter &&
        allowanceSpenderOtherUserBefore == allowanceSpenderOtherUserAfter &&
        allowanceOtherUserOwnerBefore == allowanceOtherUserOwnerAfter &&
        allowanceOtherUserSpenderBefore == allowanceOtherUserSpenderAfter,
        "Allowance should not change");

    }

    //transferBalance works
    rule transferBalanceWorks(env e){
        //FUNCTION PARAMETER
        address from;
        address to;
        require(from != to);
        address otherUser;
        require(from != otherUser && to != otherUser);
        Type.Shares amount;

        //VALUES BEFORE
        Type.Shares sharesFromBefore = getUserSharesHarness(from);
        Type.Shares sharesToBefore = getUserSharesHarness(to);
        Type.Shares sharesOtherUserBefore = getUserSharesHarness(otherUser);


        //FUNCTION CALL
        transferBalanceHarness@withrevert(e, from, to, amount);
        bool reverted = lastReverted;

        //VALUES AFTER
        Type.Shares sharesFromAfter = getUserSharesHarness(from);
        Type.Shares sharesToAfter = getUserSharesHarness(to);
        Type.Shares sharesOtherUserAfter = getUserSharesHarness(otherUser);

        //ASSERTS
        //asser1: if to = 0, revert
        assert(to == 0 => reverted, "Call should revert");

        //assert2: if sharesFromBefore < amount, revert
        assert(amount != 0 => sharesFromBefore < amount => reverted, "Call should revert");    

        //assert3: if !reverted => sharesFromAfter = sharesFromBefore - amount
        assert(!reverted && amount != 0 => to_mathint(sharesFromAfter) == sharesFromBefore - amount, "Shares should be decreased by amount");

        //assert4: if !reverted => sharesToAfter = sharesToBefore + amount
        assert(!reverted && amount != 0 => to_mathint(sharesToAfter) == sharesToBefore + amount, "Shares should be increased by amount");

        //assert5: other shares should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares should not change");

    }

    //setAllowance works
    rule setAllowanceWorks(env e){
        //FUNCTION PARAMETER
        address owner;
        address spender;
        address otherUser;
        require(otherUser != owner && otherUser != spender);
        uint256 amount;

        //VALUES BEFORE
        uint256 allowanceOwnerSpenderBefore = getAllowanceHarness(owner, spender);
        uint256 allowanceOwnerOtherUserBefore = getAllowanceHarness(owner, otherUser);
        uint256 allowanceSpenderOwnerBefore = getAllowanceHarness(spender, owner);
        uint256 allowanceSpenderOtherUserBefore = getAllowanceHarness(spender, otherUser);
        uint256 allowanceOtherUserOwnerBefore = getAllowanceHarness(otherUser, owner);
        uint256 allowanceOtherUserSpenderBefore = getAllowanceHarness(otherUser, spender);

        //FUNCTION CALL
        setAllowanceHarness@withrevert(e, owner, spender, amount);
        bool reverted = lastReverted;

        //VALUES AFTER
        uint256 allowanceAfter = getAllowanceHarness(owner, spender);
        uint256 allowanceOwnerOtherUserAfter = getAllowanceHarness(owner, otherUser);
        uint256 allowanceSpenderOwnerAfter = getAllowanceHarness(spender, owner);
        uint256 allowanceSpenderOtherUserAfter = getAllowanceHarness(spender, otherUser);
        uint256 allowanceOtherUserOwnerAfter = getAllowanceHarness(otherUser, owner);
        uint256 allowanceOtherUserSpenderAfter = getAllowanceHarness(otherUser, spender);

        //ASSERTS
        //asser1: if owner = spender, revert
        assert(owner == spender => reverted, "Call should revert");

        //assert2: if !reverted => allowanceAfter = amount
        assert(!reverted => allowanceAfter == amount, "Allowance should be set to amount");

        //assert3: other allowances should not change
        assert(allowanceOwnerOtherUserBefore == allowanceOwnerOtherUserAfter &&
        allowanceSpenderOwnerBefore == allowanceSpenderOwnerAfter &&
        allowanceSpenderOtherUserBefore == allowanceSpenderOtherUserAfter &&
        allowanceOtherUserOwnerBefore == allowanceOtherUserOwnerAfter &&
        allowanceOtherUserSpenderBefore == allowanceOtherUserSpenderAfter,
        "Allowance should not change");
    }

    //increaseBalance works
    rule increaseBalanceWorks(env e){
        //FUNCTION PARAMETER
        Type.VaultCache vaultCache;
        address account;
        address sender;
        address otherUser;
        require(otherUser != account && otherUser != sender);
        Type.Shares amount;
        Type.Assets assets;

        //VALUES BEFORE
        Type.Shares sharesAccountBefore = getUserSharesHarness(account);
        Type.Shares totalSharesBefore = getTotalSharesHarness();
        require(vaultCache.totalShares == totalSharesBefore);
        Type.Shares sharesOtherUserBefore = getUserSharesHarness(otherUser);


        //FUNCTION CALL
        increaseBalanceHarness@withrevert(e, vaultCache, account, sender, amount, assets);
        bool reverted = lastReverted;

        //VALUES AFTER
        Type.Shares sharesAccountAfter = getUserSharesHarness(account);
        Type.Shares totalSharesAfter = getTotalSharesHarness();
        Type.Shares sharesOtherUserAfter = getUserSharesHarness(otherUser);

        //ASSERTS
        //asser1: if account = 0, revert
        assert(account == 0 => reverted, "Call should revert");

        //assert2: if !reverted => sharesAccountAfter = sharesAccountBefore + amount
        assert(!reverted => to_mathint(sharesAccountAfter) == sharesAccountBefore + amount, "Shares should be increased by amount");

        //assert3: if !reverted => totalSharesAfter = totalSharesBefore + amount
        assert(!reverted => to_mathint(totalSharesAfter) == totalSharesBefore + amount, "Total shares should be increased by amount");

        //assert4: other shares should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares should not change");
    }

    //decreaseBalance works
    rule decreaseBalanceWorks(env e){
        //FUNCTION PARAMETER
        Type.VaultCache vaultCache;
        address account;
        address sender;
        address receiver;
        address otherUser;
        require(otherUser != account && otherUser != sender && otherUser != receiver);
        Type.Shares amount;
        Type.Assets assets;

        //VALUES BEFORE
        Type.Shares sharesAccountBefore = getUserSharesHarness(account);
        Type.Shares totalSharesBefore = getTotalSharesHarness();
        require(vaultCache.totalShares == totalSharesBefore);
        Type.Shares sharesOtherUserBefore = getUserSharesHarness(otherUser);



        //FUNCTION CALL
        decreaseBalanceHarness@withrevert(e, vaultCache, account, sender, receiver,amount, assets);
        bool reverted = lastReverted;

        //VALUES AFTER
        Type.Shares sharesAccountAfter = getUserSharesHarness(account);
        Type.Shares totalSharesAfter = getTotalSharesHarness();
        Type.Shares sharesOtherUserAfter = getUserSharesHarness(otherUser);

        //ASSERTS
        //asser1: if account = 0, revert
        assert(sharesAccountBefore < amount => reverted, "Call should revert");

        //assert2: if !reverted => sharesAccountAfter = sharesAccountBefore - amount
        assert(!reverted => to_mathint(sharesAccountAfter) == sharesAccountBefore - amount, "Shares should be decreased by amount");

        //assert3: if !reverted => totalSharesAfter = totalSharesBefore - amount
        assert(!reverted => to_mathint(totalSharesAfter) == totalSharesBefore - amount, "Total shares should be decreased by amount");

        //assert4: other shares should not change
        assert(sharesOtherUserBefore == sharesOtherUserAfter, "Shares should not change");
    }
    
    //onlyDecreasesUserBalance
    rule onlyDecreasesUserBalance(env e, method f, calldataarg args) filtered{ f ->
    !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)}{
        //values before
        address account;
        Type.Shares sharesBefore = getUserSharesHarness(account);

        //function call
        f(e, args);

        //values after
        Type.Shares sharesAfter = getUserSharesHarness(account);

        //asserts
        assert(sharesBefore > sharesAfter =>
        f.selector == sig:decreaseBalanceHarness(Type.VaultCache,address,address,address,Type.Shares, Type.Assets).selector ||
        f.selector == sig:transferBalanceHarness(address,address,Type.Shares).selector,
        "Should not decrease user shares");

    }

    //onlyChangeTotalShares
    rule onlyChangeTotalShares(env e, method f, calldataarg args) filtered{ f ->
    !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)}{
        //values before
        Type.Shares totalSharesBefore = getTotalSharesHarness();

        //function call
        f(e, args);

        //values after
        Type.Shares totalSharesAfter = getTotalSharesHarness();

        //asserts
        assert(totalSharesAfter > totalSharesBefore =>
        f.selector == sig:increaseBalanceHarness(Type.VaultCache,address,address,Type.Shares, Type.Assets).selector ||
        f.selector == sig:decreaseBalanceHarness(Type.VaultCache,address,address,address,Type.Shares, Type.Assets).selector,
        "Should not increase total shares");
    }

    //onlyDecreasesAllowance
    rule onlyDecreasesAllowance(env e, method f, calldataarg args) filtered{ f ->
    !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)}{
        //values before
        address owner;
        address spender;
        uint256 allowanceBefore = getAllowanceHarness(owner, spender);

        //function call
        f(e, args);

        //values after
        uint256 allowanceAfter = getAllowanceHarness(owner, spender);

        //asserts
        assert(allowanceBefore > allowanceAfter =>
        f.selector == sig:setAllowanceHarness(address,address,uint256).selector ||
        f.selector == sig:decreaseAllowanceHarness(address,address,Type.Shares).selector, "Should not decrease allowance");

    }

    //onlyIncreasesUserShares
    rule onlyIncreasesUserShares(env e, method f, calldataarg args) filtered{ f ->
    !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)}{
        //values before
        address account;
        Type.Shares sharesBefore = getUserSharesHarness(account);

        //function call
        f(e, args);

        //values after
        Type.Shares sharesAfter = getUserSharesHarness(account);

        //asserts
        assert(sharesAfter > sharesBefore =>
        f.selector == sig:increaseBalanceHarness(Type.VaultCache,address,address,Type.Shares, Type.Assets).selector ||
        f.selector == sig:transferBalanceHarness(address,address,Type.Shares).selector,
        "Should not decrease user shares");
    }

    //onlyIncreasesAllowance
    rule onlyIncreasesAllowance(env e, method f, calldataarg args) filtered{ f ->
    !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)}{
        //values before
        address owner;
        address spender;
        uint256 allowanceBefore = getAllowanceHarness(owner, spender);

        //function call
        f(e, args);

        //values after
        uint256 allowanceAfter = getAllowanceHarness(owner, spender);

        //asserts
        assert(allowanceBefore < allowanceAfter => 
        f.selector == sig:setAllowanceHarness(address,address,uint256).selector, "Should not increase allowance");
    }

   
//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//invariant totalShares == summ of all user shares
invariant totalSharesEqulasSumOfUserSharesInvariant(address alice, address bob, address charlie)
(alice != bob && alice != charlie && bob != charlie)=>
    to_mathint(getTotalSharesHarness()) == getUserSharesHarness(alice) + getUserSharesHarness(bob) + getUserSharesHarness(charlie)
    filtered{
        f -> !f.isView && !f.isPure && !BASE_HARNESS_FUNCTIONS(f)
    }
    {
        preserved increaseBalanceHarness(Type.VaultCache vaultCache,address account,address sender, Type.Shares amount, Type.Assets assets) with (env e){
            require account == alice || account == bob || account == charlie;
            require vaultCache.totalShares == getTotalSharesHarness();
        }

        preserved decreaseBalanceHarness(Type.VaultCache vaultCache,address account,address sender,address receiver, Type.Shares amount, Type.Assets assets) with (env e){
            require account == alice || account == bob || account == charlie;
            require vaultCache.totalShares == getTotalSharesHarness();
        }

        preserved transferBalanceHarness(address from, address to, Type.Shares amount) with (env e){
            require from == alice || from == bob || from == charlie;
            require to == alice || to == bob || to == charlie;
        }

}

//------------------------------- INVARIENTS OK END-------------------------------


