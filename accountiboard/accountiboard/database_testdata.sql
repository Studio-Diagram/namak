INSERT INTO accounti_user (
	first_name,
	last_name,
	phone,
	is_active,
	password,
	user_type,
	date_joined,
	home_address) 
VALUES (
	'test_first_name',
	'test_last_name',
	'0912',
	true,
	'pbkdf2_sha256$120000$eFM2jCGCoaQg$Wnziyp9xaIrKGkw9Dd3o+mFxFSgp5bMGMFTkdz5u3S0=',
	1,
	now(),
	'test home address'
);

INSERT INTO accounti_organization (
	name,
	shortcut_login_url)
VALUES (
	'test_organization',
	'test_organization_shortcut_login_url'
);


INSERT INTO accounti_cafeowner (
	user_id,
	organization_id)
VALUES (
	(SELECT id FROM accounti_user WHERE phone='0912'),
	(SELECT id FROM accounti_organization WHERE name='test_organization')
);


INSERT INTO accounti_branch (
	name,
	address,
	start_working_time,
	end_working_time,
	organization_id,
	min_paid_price,
	guest_pricing)
VALUES (
	'test_branch',
	'test_branch address',
	'09:00:00',
	'17:00:00',
	(SELECT id FROM accounti_organization WHERE name='test_organization'),
	5000,
	false
);