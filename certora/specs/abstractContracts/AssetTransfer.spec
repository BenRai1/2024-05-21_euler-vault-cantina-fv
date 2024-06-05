
using AssetTransfersHarness as AssetTransfers;
using DummyERC20A as Token;

// used to test running time
use builtin rule sanity;

methods{
    function _.safeTransferFrom(address token, address from, address to, uint256 value, address permit2) internal => CVLSaveTransferFrom(token, from, to, value) expect void; 
    function _.safeTransfer(address token, address to, uint256 value) internal with (env e) => CVLSaveTransfer(token, calledContract, to, value) expect void;
}

function CVLSaveTransferFrom(address token, address from, address to, uint256 value) {    
    require(value <= balancesGhost[token][from]);
    require(to_mathint(value) <= max_uint256 - balancesGhost[token][to]);
    balancesGhost[token][from] = assert_uint256(balancesGhost[token][from] - value);
    balancesGhost[token][to] = assert_uint256(balancesGhost[token][to] + value);
}

function CVLSaveTransfer(address token, address from, address to, uint256 value) {
    require(value <= balancesGhost[token][from]);
    require(to_mathint(value) <= max_uint256 - balancesGhost[token][to]);
    balancesGhost[token][from] = assert_uint256(balancesGhost[token][from] - value);
    balancesGhost[token][to] = assert_uint256(balancesGhost[token][to] + value);
}

ghost mapping(address => mapping (address => uint256)) balancesGhost;

//only functions who can change the state of the contract

//------------------------------- RULES TEST START ----------------------------------









//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------
    //can only change balances
    rule onlyToChangeBalances(env e, method f, calldataarg args) {
        //VALUES BEFORE
        address user;
        uint256 balanceUserBefore = balancesGhost[Token][user];

        //FUNCTION CALL
        f(e,args);

        //VALUES AFTER
        uint256 balanceUserAfter = balancesGhost[Token][user];

        //ASSERTION
        assert(balanceUserBefore != balanceUserAfter =>
        f.selector == sig:pullAssetsExt(Type.VaultCache,address,Type.Assets).selector ||
        f.selector == sig:pushAssetsExt(Type.VaultCache,address,Type.Assets).selector,
        "Only functions pullAssets and pushAssets can change balances");
    }

    //pushAssets works
    rule pushAssetsIntegrity(env e) {
        //FUNCTION PARAMETER
        Type.VaultCache vaultCache;
        require(vaultCache.asset == Token);
        address to;
        require(to != currentContract);
        Type.Assets amount;
        address otherUser;
        require(otherUser != to && otherUser != currentContract);

        //VALUES BEFORE
        Type.Assets cashBefore = vaultCache.cash;
        // Balances before
        uint256 balanceCurrentContractBefore = balancesGhost[Token][currentContract];
        uint256 balanceOtherUserBefore = balancesGhost[Token][otherUser];
        uint256 balanceToBefore = balancesGhost[Token][to];


        //FUNCTION CALL
        pushAssetsExt(e, vaultCache, to, amount);

        //VALUES AFTER
        Type.Assets cashAfter = AssetTransfers.vaultStorage.cash;
        // Balances after
        uint256 balanceCurrentContractAfter = balancesGhost[Token][currentContract];
        uint256 balanceOtherUserAfter = balancesGhost[Token][otherUser];
        uint256 balanceToAfter = balancesGhost[Token][to];

        //ASSERTS
        //assert1: cashBefore - amount == cashAfter
        assert(cashBefore - amount == to_mathint(cashAfter), "Cash should be decreased by amount");

        //assert2: balance of otherUser should not change
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of otherUser should not change");

        //assert3: balance of to should be increased by amount
        assert(balanceToBefore + amount == to_mathint(balanceToAfter), "Balance of to should be increased by amount");

        //assert4: balance of currentContract should decrease by amount
        assert(balanceCurrentContractBefore - amount == to_mathint(balanceCurrentContractAfter), "Balance of currentContract should decrease by amount");
        
    }
    //pullAssets works
    rule pullAssetsIntegrity(env e) {
        //FUNCTION PARAMETER
        Type.VaultCache vaultCache;
        require(vaultCache.asset == Token);
        address from;
        require(from != currentContract);
        Type.Assets amount;
        address otherUser;
        require(otherUser != from && otherUser != currentContract);

        //VALUES BEFORE
        Type.Assets cashBefore = vaultCache.cash;
        // Balances before
        uint256 balanceFromBefore = balancesGhost[Token][from];
        uint256 balanceOtherUserBefore = balancesGhost[Token][otherUser];
        uint256 balanceCurrentContractBefore = balancesGhost[Token][currentContract];

        //FUNCTION CALL
        pullAssetsExt(e, vaultCache, from, amount);

        //VALUES AFTER
        Type.Assets cashAfter = AssetTransfers.vaultStorage.cash;
        // Balances after
        uint256 balanceFromAfter = balancesGhost[Token][from];
        uint256 balanceOtherUserAfter = balancesGhost[Token][otherUser];
        uint256 balanceCurrentContractAfter = balancesGhost[Token][currentContract];

        //ASSERTS
        //assert1: cashBefore + amount == cashAfter
        assert(cashBefore + amount == to_mathint(cashAfter), "Cash should be increased by amount");

        //assert2: balance of otherUser should not change
        assert(balanceOtherUserBefore == balanceOtherUserAfter, "Balance of otherUser should not change");

        //assert3: balance of from should be decreased by amount
        assert(balanceFromBefore - amount == to_mathint(balanceFromAfter), "Balance of from should be decreased by amount");

        //assert4: balance of currentContract should increase by amount
        assert(balanceCurrentContractBefore + amount == to_mathint(balanceCurrentContractAfter), "Balance of currentContract should increase by amount");    
    }

    //pushAssets reverts
    rule pushAssetsRevert(env e) {
        //FUNCTION PARAMETER
        Type.VaultCache vaultCache;
        address to;
        Type.Assets amount;

        //CHECKS
        bool isKnownNonOwnerAccount = isKnownNonOwnerAccountHarness(e,to);
        bool isNotSet = isNotSetCompatibeAssetHarness(e,vaultCache.configFlags);
        
        //FUNCTION CALL
        pushAssetsExt@withrevert(e, vaultCache, to, amount);
        bool reverted = lastReverted;

        //ASSERT
        //assert1: if to == 0, then revert
        assert(to == 0 => reverted, "Revert if to == 0");

        //assert2: if siKnownNonOwnerAccount and isNotSet, then revert
        assert(isKnownNonOwnerAccount && isNotSet => reverted, "Revert if isKnownNonOwnerAccount and isNotSet");

    }

    //only functions to change vaultStorage cash
    rule onlyToChangeVaultStorageCash(env e, method f, calldataarg args) {
        //VALUES BEFORE
        Type.Assets cashBefore = AssetTransfers.vaultStorage.cash;

        //FUNCTION CALL
        f(e,args);

        //VALUES AFTER
        Type.Assets cashAfter = AssetTransfers.vaultStorage.cash;

        //ASSERTION
        assert(cashBefore != cashAfter => 
        f.selector == sig:pullAssetsExt(Type.VaultCache,address,Type.Assets).selector ||
        f.selector == sig:pushAssetsExt(Type.VaultCache,address,Type.Assets).selector,
        "Only functions pullAssets and pushAssets can change cash");
    }

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------
