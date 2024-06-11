pragma solidity ^0.8.0;
import "../../../src/EVault/modules/Borrowing.sol";
import "../../../src/EVault/shared/types/UserStorage.sol";
import "../../../src/EVault/shared/types/Types.sol";
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/shared/types/Types.sol";

uint256 constant SHARES_MASK = 0x000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFF;
uint256 constant OWED_MASK = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000;
uint256 constant OWED_OFFSET = 112;


contract BorrowingHarness is AbstractBaseHarness, Borrowing {
    using TypesLib for uint256;
    using AssetsLib for Assets;

    constructor(Integrations memory integrations) Borrowing(integrations) {}

    function initOperationExternal(uint32 operation, address accountToCheck)
        public 
        returns (VaultCache memory vaultCache, address account)
    {
        return initOperation(operation, accountToCheck);
    }

    function getTotalBalance() external view returns (Shares) {
        return vaultStorage.totalShares;
    }

    function toAssetsExt(uint256 amount) external pure returns (uint256){
        return TypesLib.toAssets(amount).toUint();
    }

    function unpackBalanceExt(PackedUserSlot data) external view returns (Shares) {
        return Shares.wrap(uint112(PackedUserSlot.unwrap(data) & SHARES_MASK));
    }

    function getUserInterestAccExt(address account) external view returns (uint256) {
        return vaultStorage.users[account].interestAccumulator;
    }

    function getVaultInterestAccExt() external returns (uint256) {
        VaultCache memory vaultCache = updateVault();
        return vaultCache.interestAccumulator;
    }

     function getUnderlyingAssetExt() external returns (IERC20) {
        VaultCache memory vaultCache = updateVault();
        return vaultCache.asset;
    }

    function OP_BORROW_Harness() external pure returns (uint32) {
        return OP_BORROW;
    }

    function CHECKACCOUNT_CALLER_Harness() external pure returns (address) {
        return CHECKACCOUNT_CALLER;
    }

    function evcHarness() external view returns (address) {
        return address(evc);
    }

    function toAssetHarness(uint256 amount) external pure returns (Assets) {
        return amount.toAssets();
    }

    function toOwedHarness(Assets self) external pure returns (Owed) {
        return self.toOwed();
    }

    function getTotalBorrowsHarness() external view returns (Owed) {
        return vaultStorage.totalBorrows;
    }


    function getUserBorrowHarness(uint256 vaultInterestAccumulator, address account) external view returns (Owed) {
        Owed prevOwed = vaultStorage.users[account].getOwed();
        if (prevOwed.isZero()) return Owed.wrap(0);

        return prevOwed.mulDiv(vaultInterestAccumulator, vaultStorage.users[account].interestAccumulator); //@audit-issue Solidity kann nicht über uint256 hinaus rechnen => wenn prevOwed * vaultInterestAccumulator is über uint256 the function will revert => not 100% sure, write a test
    }

    function getUserInterestAccumulatorHarness(address account) external view returns (uint256) {
        return vaultStorage.users[account].interestAccumulator;
    }

    function getCurrentOwedHarness(VaultCache memory vaultCache, address account) external view returns (Owed) {
        Owed owed = vaultStorage.users[account].getOwed();
        //if owed is zero, return 0
        if (owed.isZero()) return Owed.wrap(0);

        return owed.mulDiv(vaultCache.interestAccumulator, vaultStorage.users[account].interestAccumulator);
    }

    function getCurrentVaultCacheHarness() external returns (VaultCache memory){
        VaultCache memory vaultCache;
        (vaultCache.asset, vaultCache.oracle, vaultCache.unitOfAccount) = ProxyUtils.metadata();
        vaultCache.lastInterestAccumulatorUpdate = vaultStorage.lastInterestAccumulatorUpdate;
        vaultCache.cash = vaultStorage.cash;
        vaultCache.totalBorrows = vaultStorage.totalBorrows;
        vaultCache.totalShares = vaultStorage.totalShares;
        vaultCache.supplyCap = vaultStorage.supplyCap.resolve();
        vaultCache.borrowCap = vaultStorage.borrowCap.resolve();
        vaultCache.hookedOps = vaultStorage.hookedOps;
        vaultCache.snapshotInitialized = vaultStorage.snapshotInitialized;
        vaultCache.accumulatedFees = vaultStorage.accumulatedFees;
        vaultCache.configFlags = vaultStorage.configFlags;
        vaultCache.interestAccumulator = vaultStorage.interestAccumulator;
        return vaultCache;
    }

    function loadUserBorrowHarness(VaultCache calldata vaultCache, address account) external returns (Owed, Owed) {
        Owed prevOwed = vaultStorage.users[account].getOwed();
        Owed newOwed = getCurrentOwed(vaultCache, account, prevOwed);
        if (prevOwed.isZero()){
            newOwed =  Owed.wrap(0);
        } else {
            newOwed = prevOwed.mulDiv(vaultCache.interestAccumulator, vaultStorage.users[account].interestAccumulator);
        }
        return (newOwed, prevOwed);
    }

    function finalAmountDustHarness(Owed amount, Owed currentOwed) external pure returns (Owed) {
        if (
            (amount > currentOwed && amount.subUnchecked(currentOwed).isDust())
                || (amount < currentOwed && currentOwed.subUnchecked(amount).isDust())
        ) {
            return currentOwed;
        } 
        return amount;  
    }

    function repayWithSharesCalculationHarness(
        uint256 amount, Shares sharesOnBehalf, VaultCache calldata vaultCache, Assets OwedReceiverAsAssets) external returns (Assets assets, Shares shares) {
        if (amount == type(uint256).max) {
            shares = sharesOnBehalf;
            assets = shares.toAssetsDown(vaultCache);
        } else {
            shares = assets.toSharesUp(vaultCache);
            assets = amount.toAssets();
        }

        if (assets.isZero()) {
            assets = Assets.wrap(0);
            shares = Shares.wrap(0);
            return (assets, shares);
        }

        if (assets > OwedReceiverAsAssets) {
            assets = OwedReceiverAsAssets;
            shares = assets.toSharesUp(vaultCache);
        }
    }

    // function getBalanceAndBalanceForwarderHarness(UserStorage storage userStorage) internal view returns (Shares, bool) {
    //     return  (Shares.wrap(0), false); //@audit make this right
    // }

    function getUserCollateralBalanceHarness(VaultCache memory vaultcache, address user) external view returns (uint256) {
        return IERC20(vaultcache.asset).balanceOf(user);
    }





    

}