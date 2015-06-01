def auto_estimate_predictive_distributions(stringY, L_max, is_multiline = False, verbose = True):
	"""
    {Edited by Umut Eser, June 1st, 2015}
    
	Given a string of outputs,
	returns the counts associated with
	ypast
	and with 
	(ypast, yfuture),
	which allows us to estimate
		P(yfuture | ypast)
	as 
		#(ypast, yfuture)/#(ypast)
	

	Parameters
	----------
	stringY : str
			The string associated with the realization from the
			output process Y.
	L_max : int
			The maximum history length to use in inferring the
			predictive distributions.
	is_multiline : bool
			True if the input files are stored with a single
			realization per line.
	verbose : bool
			True if various warning / update messages should
			be printed.
	

	Returns
	-------
	word_lookup_marg : dict
			A dictionary that maps from the
			past of length <= L_max to the count
			of the past.
	word_lookup_fut : dict
			A dictionary that maps from the
			past + next output symbol of 
			length <= L_max to the counts of the
			number of those occurrences.

	Notes
	-----
	Any notes go here.

	Examples
	--------
	>>> import module_name
	>>> # Demonstrate code here.

	"""
	
	if is_multiline:
		Xs = copy.copy(stringX); Ys = copy.copy(stringY)

		# Counter for events (X_{t-L}^{t-1}, Y_{t-L}^{t-1})

		word_lookup_marg = Counter()

		# Counter for events (X_{t-L}^{t-1}, Y_{t-L}^{t-1}, Y_{t})

		word_lookup_fut  = Counter()
		
		if verbose:
			print 'Estimating predictive distributions using multi-line.'
		
		for line_ind in range(len(Ys)):
            stringY = Ys[line_ind]

			Ty = len(stringY)

			T = Ty

			for t_ind in range(T-L_max):
				cur_stringY = stringY[t_ind:(t_ind + L_max + 1)]
	
				word_lookup_marg[cur_stringY[:-1]] += 1
				word_lookup_fut[cur_stringY] += 1
	
				# for remove_inds in range(0, L_max+1): DON'T NEED THIS
				for remove_inds in range(1, L_max+1):
					trunc_stringY = cur_stringY[:-remove_inds]
					word_lookup_marg[trunc_stringY[:-1]] += 1
					word_lookup_fut[trunc_stringY] += 1
			
			# DON'T NEED THIS
			
			# word_lookup_marg[('', '')] = word_lookup_fut[('', '')] # Since we double count ('', '') in the loop above, we need to for the marginal case, fix it.
	else:

		Ty = len(stringY)

		T = Tx

		# Counter for events (X_{t-L}^{t-1}, Y_{t-L}^{t-1})

		word_lookup_marg = Counter()

		# Counter for events (X_{t-L}^{t-1}, Y_{t-L}^{t-1}, Y_{t})

		word_lookup_fut  = Counter()
		
		if verbose:
			print 'Estimating predictive distributions.'

		for t_ind in range(T-L_max):

			cur_stringY = stringY[t_ind:(t_ind + L_max + 1)]

			word_lookup_marg[cur_stringY[:-1]] += 1
			word_lookup_fut[cur_stringY] += 1

			for remove_inds in range(1, L_max+1):
				trunc_stringY = cur_stringY[:-remove_inds]

				word_lookup_marg[trunc_stringY[:-1]] += 1
				word_lookup_fut[trunc_stringY] += 1
    return word_lookup_marg, word_lookup_fut