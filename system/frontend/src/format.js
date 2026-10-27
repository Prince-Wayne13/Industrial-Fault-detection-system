// Two initials from a full name, for the round avatar.
export const initials = (name) => name.split(' ').map((w) => w[0]).slice(0, 2).join('')
