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

    // function getNewOwedHarness(PackedUserSlot data, Owed owed) external pure returns (PackedUserSlot) {
    //     uint256 data = PackedUserSlot.unwrap(data);

    //     return PackedUserSlot.wrap((owed.toUint() << OWED_OFFSET) | (data & ~OWED_MASK));
    // }

    function getUserBorrowHarness(uint256 vaultInterestAccumulator, address account) external view returns (Owed) {
        Owed prevOwed = vaultStorage.users[account].getOwed();
        if (prevOwed.isZero()) return Owed.wrap(0);

        return prevOwed.mulDiv(vaultInterestAccumulator, vaultStorage.users[account].interestAccumulator); //@audit-issue Solidity kann nicht über uint256 hinaus rechnen => wenn prevOwed * vaultInterestAccumulator is über uint256 the function will revert => not 100% sure, write a test
    }

    function getUserInterestAccumulatorHarness(address account) external view returns (uint256) {
        return vaultStorage.users[account].interestAccumulator;
    }

}