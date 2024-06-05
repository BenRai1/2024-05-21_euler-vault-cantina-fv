// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

//import the abstarct contract
import "../../../src/EVault/shared/AssetTransfers.sol";
import "../AbstractBaseHarness.sol";

contract AssetTransfersHarness is AssetTransfers, AbstractBaseHarness {

    constructor(Integrations memory integrations) Base(integrations) {}

    function pullAssetsExt(VaultCache memory vaultCache, address from, Assets amount) public {
        pullAssets(vaultCache, from, amount);
    }

    function pushAssetsExt(VaultCache memory vaultCache, address to, Assets amount) public {
        pushAssets(vaultCache, to, amount);
    }
}
