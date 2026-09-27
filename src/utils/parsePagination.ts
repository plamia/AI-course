export interface PaginationQuery {
    page: number;
    limit: number;
    severity?: 'INFO' | 'WARN' | 'ERROR';
  }
  
  export function parsePaginationQuery(query: Record<string, unknown>): PaginationQuery {
    const parseVal = (val: unknown): string | undefined => {
      if (Array.isArray(val)) {
        if (val.length === 0) return undefined;
        return typeof val[0] === 'string' ? val[0] : String(val[0]);
      }
      if (typeof val === 'string') return val;
      return undefined;
    };
  
    const rawPage = parseInt(parseVal(query.page) || '1', 10);
    const rawLimit = parseInt(parseVal(query.limit) || '20', 10);
    const rawSeverity = parseVal(query.severity)?.toUpperCase();
  
    const page = !isNaN(rawPage) && rawPage > 0 ? rawPage : 1;
    let limit = !isNaN(rawLimit) && rawLimit > 0 ? rawLimit : 20;
    if (limit > 100) limit = 100;
  
    let severity: PaginationQuery['severity'] = undefined;
    if (rawSeverity) {
      if (['INFO', 'WARN', 'ERROR'].includes(rawSeverity)) {
        severity = rawSeverity as PaginationQuery['severity'];
      } else {
        throw new Error('INVALID_SEVERITY');
      }
    }
  
    return { page, limit, severity };
  }