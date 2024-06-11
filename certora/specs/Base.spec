import "./Base/base.spec";

// using BaseHarness as Base; //@audit does not work for other specs because BaseHarness is not in the scene

//------------------------------- RULES TEST START ----------------------------------

// //updateVault works
// rule updateVaultWorks(env e) {
//     //require
//     require(e.block.timestamp <= max_uint48);

//     //TARGET VALUES 
//     Type.VaultCache vaultCacheBefore = loadVaultHarness(e);
//     address assetTarget = vaultCacheBefore.asset; 
//     address oracleTarget = vaultCacheBefore.oracle;
//     address unitOfAccountTarget = vaultCacheBefore.unitOfAccount;
//     // Vault config
//     uint256 supplyCapTarget = vaultCacheBefore.supplyCap;
//     uint256 borrowCapTarget = vaultCacheBefore.borrowCap;
//     Type.Flags hookedOpsTarget = vaultCacheBefore.hookedOps;
//     Type.Flags configFlagsTarget = vaultCacheBefore.configFlags;
//     // Runtime
//     bool snapshotInitializedTarget = vaultCacheBefore.snapshotInitialized;
//     // Vault data
//     Type.Assets cashTarget = vaultCacheBefore.cash; 
//     uint48 lastInterestAccumulatorUpdateTarget = require_uint48(e.block.timestamp);
//     Type.Owed totalBorrowsTarget;//@audit 
//     Type.Shares totalSharesTarget;//@audit 
//     Type.Shares accumulatedFeesTarget;//@audit 
//     uint256 interestAccumulatorTarget;//@audit 

//     //VALUES before
//     bool dirty = to_mathint(e.block.timestamp) > to_mathint(vaultCacheBefore.lastInterestAccumulatorUpdate);

//     //FUNCTIONCALL
//     Type.VaultCache vaultCacheCall = updateVaultHarness(e);

//     //VALUES AFTER
//     Type.Owed totalBorrowsStorageAfter = Base.vaultStorage.totalBorrows; 
//     Type.Shares totalSharesStorageAfter = Base.vaultStorage.totalShares; 
//     Type.Shares accumulatedFeesStorageAfter = Base.vaultStorage.accumulatedFees;
//     uint256 interestAccumulatorStorageAfter = Base.vaultStorage.interestAccumulator;

//      Type.VaultCache vaultCacheAfter = loadVaultHarness(e);





//     //ASSERTS
//     // //assert 1: the right values are returned //@audit timeout on its own
//     // assert(vaultCacheCall.asset == assetTarget &&
//     // vaultCacheCall.oracle == oracleTarget &&
//     // vaultCacheCall.unitOfAccount == unitOfAccountTarget &&
//     // vaultCacheCall.supplyCap == supplyCapTarget &&
//     // vaultCacheCall.borrowCap == borrowCapTarget &&
//     // vaultCacheCall.hookedOps == hookedOpsTarget &&
//     // vaultCacheCall.configFlags == configFlagsTarget &&
//     // vaultCacheCall.snapshotInitialized == snapshotInitializedTarget &&
//     // vaultCacheCall.cash == cashTarget &&
//     // vaultCacheCall.lastInterestAccumulatorUpdate == lastInterestAccumulatorUpdateTarget
//     // , "Returned values are not the target values");


//     // //assert 2: if dirty, the storage variables are updated//@audit timeout on its own
//     // assert(dirty =>
//     // vaultCacheCall.lastInterestAccumulatorUpdate == lastInterestAccumulatorUpdateTarget &&
//     // vaultCacheCall.accumulatedFees == accumulatedFeesStorageAfter &&
//     // vaultCacheCall.totalShares == totalSharesStorageAfter &&
//     // vaultCacheCall.totalBorrows == totalBorrowsStorageAfter &&
//     // to_mathint(vaultCacheCall.interestAccumulator) == to_mathint(interestAccumulatorStorageAfter), "The storage variables were not updated");



//     //-------------------ASSERTS OK START --------------------------

//     //assert 3: all other variables stay the same
//     assert(vaultCacheBefore.asset == vaultCacheAfter.asset &&
//     vaultCacheBefore.oracle == vaultCacheAfter.oracle &&
//     vaultCacheBefore.unitOfAccount == vaultCacheAfter.unitOfAccount &&
//     vaultCacheBefore.supplyCap == vaultCacheAfter.supplyCap &&
//     vaultCacheBefore.borrowCap == vaultCacheAfter.borrowCap &&
//     vaultCacheBefore.hookedOps == vaultCacheAfter.hookedOps &&
//     vaultCacheBefore.configFlags == vaultCacheAfter.configFlags &&
//     vaultCacheBefore.snapshotInitialized == vaultCacheAfter.snapshotInitialized &&
//     vaultCacheBefore.cash == vaultCacheAfter.cash, "This values should not have changed");

//     //-------------------ASSERTS OK END --------------------------

// }

//------------------------------- RULES TEST END ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES PROBLEMS START ----------------------------------

//------------------------------- RULES OK START ------------------------------------

//------------------------------- RULES OK END ------------------------------------

//------------------------------- INVARIENTS OK START-------------------------------

//------------------------------- INVARIENTS OK END-------------------------------

//------------------------------- ISSUES OK START-------------------------------

//------------------------------- ISSUES OK END-------------------------------




