import pandas as pd
from rich import print

def analyze_results(trades: list[dict]):
    if not trades:
        print("[yellow]No trades executed.[/yellow]")
        return
    df = pd.DataFrame(trades)
    pnl = (df["cash_delta"]).sum()
    wins = (df["cash_delta"] > 0).sum()
    losses = (df["cash_delta"] <= 0).sum()
    win_rate = wins / max(1, (wins + losses))
    avg_gain = df.loc[df["cash_delta"] > 0, "cash_delta"].mean()
    avg_loss = df.loc[df["cash_delta"] <= 0, "cash_delta"].mean()
    print(f"[bold cyan]Total PnL:[/bold cyan] {pnl:.2f}")
    print(f"Win rate: {win_rate:.2%}")
    print(f"Avg gain: {avg_gain:.2f} | Avg loss: {avg_loss:.2f}")
