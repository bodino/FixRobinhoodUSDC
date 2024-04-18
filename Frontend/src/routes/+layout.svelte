<script>
    import { onMount } from "svelte";

    let nonZeroBalances = {};
    let unsignedTransactions = [];
    let totalValue = 0;
    let costToReturnFunds = 0;

    onMount(async () => {
        const balancesResponse = await fetch("/non_zero_balances.json");
        nonZeroBalances = await balancesResponse.json();
        totalValue = Object.values(nonZeroBalances).reduce(
            (sum, value) => sum + value,
            0,
        );
        totalValue = totalValue * 10 ** -6; // Convert to more readable format assuming USDC.e

        const transactionsResponse = await fetch("/unsigned_transactions.json");
        unsignedTransactions = await transactionsResponse.json();

        costToReturnFunds = unsignedTransactions.length * 0.002; // Example calculation for cost
        unsignedTransactions = unsignedTransactions.sort((a, b) => {
            const balanceA = nonZeroBalances[a.from] || 0;
            const balanceB = nonZeroBalances[b.from] || 0;
            return balanceB - balanceA; // Descending order
        });
    });
</script>

<div class="container">
    <div class="box overview">
        <h1 style="font-weight: bolder; font-size: 50px;">
            Fix Robinhood Overview
        </h1>
        <div class="stat">
            <p class="label">Number of Users Affected</p>
            <p class="value">{Object.keys(nonZeroBalances).length}</p>
        </div>
        <div class="stat">
            <p class="label">Total Value Held</p>
            <p class="value">${totalValue.toLocaleString("en-US")} USD</p>
        </div>
        <div class="stat">
            <p class="label">Cost to Return Funds</p>
            <p class="value">{costToReturnFunds.toFixed(3)} USD</p>
        </div>
    </div>

    <div class="box explanation">
        <p>
            Robinhood users, including myself, are facing a predicament where
            USDC.e tokens sent to Robinhood remain inaccessible due to a
            transition from USDC.e support to a new USDC. Despite numerous
            attempts to resolve the issue through customer support and
            regulatory pathways, the funds have not been credited back. The
            underlying cause is a lack of clear communication regarding the
            distinction between USDC and USDC.e, leaving users' funds in limbo.
            My extensive analysis has revealed 372 affected users with
            approximately $81,000 in USDC.e stuck with Robinhood. To rectify
            this, I've prepared the transactions necessary for recovery and am
            taking legal action to reclaim the funds. The resolution of this
            issue highlights systemic flaws that need addressing to prevent
            future occurrences.
        </p>
    </div>

    <div class="responsive-table">
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Value (USDC.e)</th>
                </tr>
            </thead>
            <tbody>
                {#each unsignedTransactions as tx}
                    {#if nonZeroBalances[tx.from] / 1000000 > 5}
                        <tr>
                            <td>{tx.from}</td>
                            <td>
                                {parseInt(
                                    nonZeroBalances[tx.from] / 1000000,
                                ).toLocaleString("en-US")}
                            </td>
                        </tr>
                    {/if}
                {/each}
            </tbody>
        </table>
    </div>
</div>

<div class="download-buttons">
    <a
        href="/non_zero_balances.json"
        download="non_zero_balances.json"
        class="button">Download Non-Zero Balances</a
    >
    <a
        href="/unsigned_transactions.json"
        download="unsigned_transactions.json"
        class="button">Download Unsigned Transactions</a
    >
</div>

<div class="github-link">
    <a
        href="https://github.com/yourusername/your-repo-name"
        target="_blank"
        class="button">View on GitHub</a
    >
</div>

<style>
    body {
        font-family: "Arial", sans-serif;
        background-color: #000000; /* Robinhood's dark theme background */
        color: #ffffff; /* White text for high contrast */
        margin: 0;
        padding: 0;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 20px;
        margin-top: 50px; /* Space from top */
        box-sizing: border-box;
    }

    .box {
        background: #ffffff; /* White background for content boxes */
        color: #333; /* Dark text for content */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        width: 90%; /* Responsive width */
        max-width: 600px; /* Max width for larger screens */
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    .overview {
        background-color: #21ce99; /* Robinhood green for the overview box */
        color: #ffffff; /* White text for overview box */
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
    }

    h1 {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 30px;
    }

    .stat {
        margin-bottom: 15px;
    }

    .label {
        font-size: 2em;
        font-weight: 600;
    }

    .value {
        font-size: 2.4em;
        font-weight: 700;
        color: #fcdc00; /* Bright yellow for values */
    }

    .explanation {
        background: #333; /* Dark background for contrast */
        color: #ffffff; /* White text for readability */
    }

    .responsive-table {
        overflow-x: auto; /* Scroll on small screens */
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th,
    td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
        word-wrap: break-word; /* Wrap text in cells */
    }

    th {
        background-color: #21ce99; /* Robinhood green for table headers */
        color: white;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2; /* Light background for even rows */
        color: #333; /* Dark text for even rows */
    }
    .download-buttons,
    .github-link {
        text-align: center;
        margin-top: 20px;
    }

    .button {
        display: inline-block;
        margin: 10px;
        padding: 10px 15px;
        border-radius: 5px;
        background-color: #21ce99; /* Robinhood green */
        color: #ffffff;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }

    .button:hover {
        background-color: #1b8d76; /* Darker green on hover */
    }
</style>
