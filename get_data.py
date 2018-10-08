import os

from blockchain import blockexplorer
import pandas as pd


blocks_heights = range(100)

if not os.path.isfile('./cash_flows.pkl'):
    # get blocks and corresponding transaction hash list
    blocks = []
    for block_height in blocks_heights:
        blocks += blockexplorer.get_block_height(block_height)

    transactions_hash_list = []
    for block in blocks:
        transactions_hash_list += [tx.hash for tx in block.transactions]

    # get corresponding transactions data
    transactions = []
    for tx_id in transactions_hash_list:
        transactions.append(blockexplorer.get_tx(tx_id))

    # save corresponding cash flows per user
    cash_flows = []
    for transaction in transactions:
        # get transaction cash flows
        for input_ in transaction.inputs:
            if hasattr(input_, 'address'):
                cash_flows.append([input_.address, transaction.time, -input_.value])
        for output_ in transaction.outputs:
            if hasattr(output_, 'address'):
                cash_flows.append([output_.address, transaction.time, +output_.value])

    # converts it to df
    df = pd.DataFrame(cash_flows, columns=['user', 'time', 'value'])
    df.to_pickle("./cash_flows.pkl")
