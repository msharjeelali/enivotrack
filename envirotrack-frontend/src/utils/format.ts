export const fmtDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-PK', { day: '2-digit', month: 'short', year: 'numeric' });

export const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString('en-PK', { hour: '2-digit', minute: '2-digit' });

export const fmtDateTime = (iso: string) => `${fmtDate(iso)} ${fmtTime(iso)}`;
export const fmtPct = (val: number) => `${Math.round(val * 100)}%`;
export const fmtNum = (n: number) => n.toLocaleString();
export const fmtCurrency = (n: number) => `PKR ${n.toLocaleString()}`;
