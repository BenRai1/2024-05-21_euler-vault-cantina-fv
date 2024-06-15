// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

//import the abstarct contract
import "../../../src/EVault/shared/BorrowUtils.sol";
import "../AbstractBaseHarness.sol";

contract BorrowUtilsHarness is BorrowUtils, AbstractBaseHarness {

    constructor(Integrations memory integrations) Base(integrations) {}

    function getCurrentOwedHarness(VaultCache memory vaultCache, address account) public view returns (Owed) {
        return getCurrentOwed(vaultCache, account);
    }

    function increaseBorrowHarness(VaultCache memory vaultCache, address account, Assets assets) public {
        increaseBorrow(vaultCache, account, assets);
    }

    function decreaseBorrowHarness(VaultCache memory vaultCache, address account, Assets assets) public {
        decreaseBorrow(vaultCache, account, assets);
    }

    function transferBorrowHarness(VaultCache memory vaultCache, address from, address to, Assets assets) public {
        transferBorrow(vaultCache, from, to, assets);
    }

    function computeInterestRateHarness(VaultCache memory vaultCache) public returns (uint256) {
        return computeInterestRate(vaultCache);
    }

    function currentUserBorrowHarness(VaultCache memory vaultCache, address account) public view returns (Owed) {
        Owed owed = vaultStorage.users[account].getOwed();
        if (owed.isZero()) return Owed.wrap(0);
        return owed.mulDiv(vaultCache.interestAccumulator, vaultStorage.users[account].interestAccumulator);
    }

    function getTotalBorrowsHarness() public view returns (Owed) {
        return vaultStorage.totalBorrows;
    }

    function getUserInterestAccumulatorHarness(address account) external view returns (uint256) {
        return vaultStorage.users[account].interestAccumulator;
    }

    function getGlobalInterestAccumulatorHarness() external view returns (uint256) {
        return vaultStorage.interestAccumulator;
    }

}