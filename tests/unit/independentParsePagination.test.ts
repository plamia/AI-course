import { describe, it, expect } from 'vitest';
import { parsePaginationQuery } from '../../src/utils/parsePagination';

describe('Independent Verification: parsePaginationQuery()', () => {
  // AC-1: Default Fallbacks
  describe('AC-1: Default values for missing parameters', () => {
    it('should return page=1 and limit=20 when query is empty', () => {
      const result = parsePaginationQuery({});
      expect(result).toEqual({ page: 1, limit: 20, severity: undefined });
    });

    it('should return page=1 and limit=20 when query parameters are undefined', () => {
      const result = parsePaginationQuery({ page: undefined, limit: undefined });
      expect(result).toEqual({ page: 1, limit: 20, severity: undefined });
    });
  });

  // AC-2: Valid Custom Bounds
  describe('AC-2: Parsing valid custom page and limit values', () => {
    it('should correctly parse valid page and limit numbers passed as strings', () => {
      const result = parsePaginationQuery({ page: '3', limit: '50' });
      expect(result).toEqual({ page: 3, limit: 50, severity: undefined });
    });
  });

  // AC-3: Out-of-Bounds & Invalid Numeric Handling
  describe('AC-3: Handling out-of-bounds or non-numeric pagination inputs', () => {
    it('should clamp limit to maximum 100 when requested limit exceeds 100', () => {
      const result = parsePaginationQuery({ limit: '500' });
      expect(result.limit).toBe(100);
    });

    it('should fallback page to 1 when page is zero or negative', () => {
      const result = parsePaginationQuery({ page: '-5' });
      expect(result.page).toBe(1);
    });

    it('should fallback to defaults when page/limit are non-numeric strings', () => {
      const result = parsePaginationQuery({ page: 'invalid', limit: 'foo' });
      expect(result.page).toBe(1);
      expect(result.limit).toBe(20);
    });
  });

  // AC-4: Severity Filtering
  describe('AC-4: Valid Severity Filtering', () => {
    it('should parse valid uppercase severity parameter', () => {
      const result = parsePaginationQuery({ severity: 'ERROR' });
      expect(result.severity).toBe('ERROR');
    });

    it('should normalize lowercase severity string to uppercase', () => {
      const result = parsePaginationQuery({ severity: 'warn' });
      expect(result.severity).toBe('WARN');
    });
  });

  // AC-5: Invalid Severity & Edge Cases
  describe('AC-5: Invalid Severity Handling & Boundary Edge Cases', () => {
    it('should throw INVALID_SEVERITY error on unsupported severity string', () => {
      expect(() => parsePaginationQuery({ severity: 'CRITICAL' })).toThrow('INVALID_SEVERITY');
    });

    // FLAG: Spec does not explicitly define behavior when floating-point string is passed (e.g. page=2.5)
    it('should truncate floating point page string to integer', () => {
      const result = parsePaginationQuery({ page: '2.8' });
      expect(result.page).toBe(2);
    });

    // FLAG: Spec does not define behavior for duplicate query parameters (Express array parameters)
    it('should extract first element if query param arrives as array', () => {
      const result = parsePaginationQuery({ limit: ['15', '30'] });
      expect(result.limit).toBe(15);
    });
  });
});