import { cameras, challans, settings, users, vehicles, violations, warnings } from '@/services/mocks/data';

export const violationsService = {
  async list() { return violations; },
  async getById(id: string) { return violations.find((item) => item.id === id) ?? null; },
};

export const challansService = {
  async list() { return challans; },
  async getById(id: string) { return challans.find((item) => item.id === id) ?? null; },
};

export const warningsService = {
  async list() { return warnings; },
};

export const camerasService = {
  async list() { return cameras; },
};

export const vehiclesService = {
  async list() { return vehicles; },
  async getByPlate(plate: string) { return vehicles.find((item) => item.plateText === plate) ?? null; },
};

export const usersService = {
  async list() { return users; },
};

export const settingsService = {
  async get() { return settings; },
};
