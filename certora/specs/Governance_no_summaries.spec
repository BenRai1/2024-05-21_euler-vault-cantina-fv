import "./Base.spec";
import "./Base/governance_no_summaries.spec";
using MockHookTarget as HookTarget;
using ProtocolConfig as ProtocolConfig;

// used to test running time
use builtin rule sanity;
use rule privilegedOperation;

    //convertFees reverts 
    rule convertFeesRevertIntegraty(env e) { 
        //GENERAL VARIABLES
        address actualCaller = actualCaller(e);
        address user;
            
        //VALUES BEFORE
        GovernanceHarness.VaultCache vaultCacheBefore = getVaultCacheHarness(e);
        address protocolReceiver;
        uint16 protocolFee;
        (protocolReceiver, protocolFee) = ProtocolConfig.protocolFeeConfig(e,currentContract);
        //Balances
        GovernanceHarness.PackedUserSlot userDataBefore = getUserStorageDataHarness(user);
        bool opSet = isConvertFeesSet(e, vaultCacheBefore.hookedOps);
        address hookTarget = getHookTargetHarness();

        //FUNCTION CALL
        convertFees@withrevert(e);
        bool reverted = lastReverted;

        //VALUES AFTER
        GovernanceHarness.VaultCache vaultCacheAfter = getVaultCacheHarness(e);
        GovernanceHarness.PackedUserSlot userDataAfter = getUserStorageDataHarness(user);


        //ASSERTS
        //assert1: if hook target is zero address, revert
        assert(actualCaller == 0 => reverted, "ActualCaller is 0");


        //assert2: if vaultCache.accumulatedFees = 0, stuff should not change
        assert(vaultCacheBefore.accumulatedFees == 0 => 
        vaultCacheBefore.accumulatedFees == vaultCacheAfter.accumulatedFees &&
        userDataBefore == userDataAfter,
        "Accumulated fees or balances changed");
        
        //assert3: if the protocolReceiver = 0 address, revert
        assert(vaultCacheBefore.accumulatedFees != 0 && protocolReceiver == 0 && protocolFee != 0 => reverted, "Protocol receiver is 0");

        // //assert4: if opSet && hookTarget == 0, revert
        // assert(opSet && hookTarget == 0 => reverted, "opSet and hookTarget is 0 => Function should revert");

    }